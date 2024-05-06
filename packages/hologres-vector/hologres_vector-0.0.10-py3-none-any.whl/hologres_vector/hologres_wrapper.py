from __future__ import annotations

import json
import logging
from typing import Any, ClassVar

import psycopg2


def _get_filter_clause(
    metadata_filters: dict[str, str] | None = None,
    schema_data_filters: dict[str, str] | None = None,
) -> tuple[str, list]:
    params = []
    filter_clause = ""
    conjuncts = []
    if metadata_filters is not None:
        for key, val in metadata_filters.items():
            conjuncts.append("metadata->>%s=%s")
            params.append(key)
            params.append(val)

    if schema_data_filters is not None:
        for key, val in schema_data_filters.items():
            conjuncts.append(f"{key}=%s")
            params.append(val)

    if len(conjuncts) != 0:
        filter_clause = "where " + " and ".join(conjuncts)

    return filter_clause, params


class HologresWrapper:
    DISTANCE_METHOD_TO_FUNC_NAME: ClassVar[dict[str, str]] = {
        "SquaredEuclidean": "pm_approx_squared_euclidean_distance",
        "Euclidean": "pm_approx_euclidean_distance",
        "InnerProduct": "pm_approx_inner_product_distance",
    }
    DISTANCE_METHOD_TO_SORT_ORDER: ClassVar[dict[str, str]] = {
        "SquaredEuclidean": "asc",
        "Euclidean": "asc",
        "InnerProduct": "desc",
    }

    def __init__(
        self,
        connection_string: str,
        ndims: int,
        table_name: str,
        distance_method: str,
        logger: logging.Logger | None = None,
    ) -> None:
        self.table_name = table_name
        self.conn = psycopg2.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = False
        self.ndims = ndims
        self.table_schema = {}
        self.distance_method = distance_method
        self.logger = logger or logging.getLogger(__name__)

    def create_vector_extension(self) -> None:
        self.cursor.execute("create extension if not exists proxima")
        self.conn.commit()

    def create_table(self, table_schema: dict[str, str] | None = None, drop_if_exist: bool = True) -> None:
        if table_schema is None:
            table_schema = {}
        self.table_schema = table_schema
        if drop_if_exist:
            self.cursor.execute(f"drop table if exists {self.table_name}")
        self.conn.commit()

        create_table_ddl = f"""create table if not exists {self.table_name} (id text primary key,
vector float4[] check(array_ndims(vector) = 1 and array_length(vector, 1) = {self.ndims}),
metadata json"""
        if table_schema:
            for col_name, col_type in table_schema.items():
                create_table_ddl += f", {col_name} {col_type}"
        create_table_ddl += ");"

        table_property_proxima_vectors = {
            "vector": {
                "algorithm": "Graph",
                "distance_method": self.distance_method,
                "builder_params": {
                    "min_flush_proxima_row_count": 1,
                    "min_compaction_proxima_row_count": 1,
                    "max_total_size_to_merge_mb": 2000,
                },
            }
        }

        table_property_ddl = (
            f"call set_table_property('{self.table_name}', "
            f"'proxima_vectors', '{json.dumps(table_property_proxima_vectors)}');"
        )

        self.logger.info(f"Creating table, sql: {create_table_ddl}")
        self.cursor.execute(create_table_ddl)
        self.logger.info(f"Configuring vector properties, sql: {table_property_ddl}")
        self.cursor.execute(table_property_ddl)
        self.conn.commit()

    def get_by_id(self, id: str) -> list[tuple]:
        statement = "select id, vector, metadata, document from %s where id = %s;"
        self.cursor.execute(
            statement,
            (self.table_name, id),
        )
        self.conn.commit()
        return self.cursor.fetchall()

    def batch_upsert(
        self,
        ids: list[str],
        vectors: list[list[float]],
        metadatas: list[dict],
        schema_datas: list[dict[str, str]],
    ) -> None:
        default_batch_size = 512
        remaining_rows = len(vectors)
        current_pos = 0
        schema_keys = list(self.table_schema.keys())
        all_keys = ["id", "vector", "metadata", *schema_keys]
        while remaining_rows > 0:
            batch_size = min(default_batch_size, remaining_rows)
            sql = f"insert into {self.table_name}("
            sql += ", ".join(all_keys)
            sql += ") values "
            params = []
            first = True
            for i in range(current_pos, current_pos + batch_size):
                if first:
                    first = False
                else:
                    sql += ", "
                sql += f"(%s, array{json.dumps(vectors[i])}::float4[], %s"
                for _ in schema_keys:
                    sql += ", %s"
                sql += ")"
                params.append(ids[i] if ids[i] is not None else "null")
                params.append(json.dumps(metadatas[i]))
                for key in schema_keys:
                    if key in schema_datas[i]:
                        params.append(schema_datas[i][key])
                    else:
                        params.append(None)
            remaining_rows -= batch_size
            current_pos += batch_size

            # when primary key `id` is conflicted, update the entire row.
            # https://help.aliyun.com/zh/hologres/user-guide/insert-on-conflict
            sql += " on conflict (id) do update set ("
            sql += ", ".join(all_keys)
            sql += ") = ROW (excluded.*)"

            self.cursor.execute(sql, tuple(params))
            self.conn.commit()

    def query_nearest_neighbours(
        self,
        vector: list[float],
        k: int,
        select_columns: list[str] | None = None,
        metadata_filters: dict[str, str] | None = None,
        schema_data_filters: dict[str, str] | None = None,
    ) -> list[tuple[Any, ...]]:
        """
        Return: list[id, metadata::text, distance, select_column_0, ... , select_column_n]
        """
        filter_clause, params = _get_filter_clause(metadata_filters, schema_data_filters)

        col_names = ""
        if select_columns is not None:
            for col_name in select_columns:
                col_names += f", {col_name}"

        sql = (
            f"select id, metadata::text, "
            f"{self.DISTANCE_METHOD_TO_FUNC_NAME[self.distance_method]}("
            f"vector, array{json.dumps(vector)}::float4[]) as distance {col_names} "
            f"from {self.table_name} {filter_clause} "
            f"order by distance {self.DISTANCE_METHOD_TO_SORT_ORDER[self.distance_method]} limit %s;"
        )
        self.logger.info(f"Query nearset neighbours, sql: {sql}, params: {params}, top_k: {k}")
        self.cursor.execute(sql, (*params, k))
        self.conn.commit()
        return self.cursor.fetchall()

    def query_by_filters(
        self,
        select_columns: list[str] | None = None,
        metadata_filters: dict[str, str] | None = None,
        schema_data_filters: dict[str, str] | None = None,
        limit: int = 100,
    ) -> list[tuple[Any, ...]]:
        """
        Return: list[id, vector, metadata::text, select_column_0, ... , select_column_n]
        """
        filter_clause, params = _get_filter_clause(metadata_filters, schema_data_filters)

        col_names = ""
        if select_columns is not None:
            for col_name in select_columns:
                col_names += f", {col_name}"

        sql = f"select id, vector, metadata::text {col_names} from {self.table_name} {filter_clause} limit %s;"
        self.logger.info(f"Query by filters, sql: {sql}, params: {params}")
        self.cursor.execute(sql, (*params, limit))
        self.conn.commit()
        return self.cursor.fetchall()

    def delete_by_filters(
        self,
        metadata_filters: dict[str, str] | None = None,
        schema_data_filters: dict[str, str] | None = None,
    ) -> None:
        filter_clause, params = _get_filter_clause(metadata_filters, schema_data_filters)

        sql = ""
        if filter_clause != "":
            sql = f"delete from {self.table_name} {filter_clause}"
        else:
            self.logger.info(f"Using TRUNCATE to delete all data in table {self.table_name}.")
            sql = f"truncate table {self.table_name}"

        self.cursor.execute(sql, tuple(params))
        self.conn.commit()

    def run_sql(self, sql, fetch_results=True):
        self.cursor.execute(sql)
        self.conn.commit()
        if fetch_results:
            return self.cursor.fetchall()

    def size(self) -> int:
        sql = f"select count(1) from {self.table_name}"
        return self.run_sql(sql)[0][0]
