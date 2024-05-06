from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from hologres_vector.hologres_wrapper import HologresWrapper


class HologresVector:
    """VectorStore implementation using Hologres.

    - `connection_string` is a hologres connection string. Call `connection_string_from_db_params` to generate.
    - `ndims` is the number of dimensions of the vector
    - `table_name` is the name of the table to store vector and json data.
        - NOTE: The table will be created when initializing the store (if not exists)
            So, make sure the user has the right permissions to create tables.
    - `table_schema` defines the types of the other columns of the table.
        - Useful for storing original texts other other information related to a vector.
    - `pre_delete_table` if True, will delete the table if it exists.
        (default: False)
        - Useful for testing.
    """

    def __init__(
        self,
        connection_string: str,
        ndims: int,
        table_name: str,
        table_schema: dict[str, str] | None = None,
        distance_method: str = "SquaredEuclidean",
        pre_delete_table: bool = False,
        logger: logging.Logger | None = None,
    ) -> None:
        self.connection_string = connection_string
        self.ndims = ndims
        self.table_name = table_name
        self.table_schema = table_schema
        self.distance_method = distance_method
        self.pre_delete_table = pre_delete_table
        self.logger = logger or logging.getLogger(__name__)
        self.__post_init__()

    def __post_init__(
        self,
    ) -> None:
        """
        Initialize the store.
        """
        self.storage = HologresWrapper(
            self.connection_string, self.ndims, self.table_name, self.distance_method, self.logger
        )
        self.__create_vector_extension()
        self.storage.create_table(self.table_schema, self.pre_delete_table)

    def __create_vector_extension(self) -> None:
        try:
            self.storage.create_vector_extension()
        except Exception as e:
            self.logger.exception(e)
            raise e

    def upsert_vectors(
        self,
        vectors: list[list[float]],
        ids: list[str] | None = None,
        metadatas: list[dict] | None = None,
        schema_datas: list[dict[str, str]] | None = None,
    ) -> None:
        """Add vectors to the vectorstore.

        Args:
            vectors: List of vectors.
            metadatas: List of metadatas associated with the vectors.
        """
        if ids is None:
            ids = [str(uuid.uuid1()) for _ in vectors]
        if metadatas is None:
            metadatas = [{} for _ in vectors]
        if schema_datas is None:
            schema_datas = [{} for _ in vectors]
        try:
            self.storage.batch_upsert(ids, vectors, metadatas, schema_datas)
        except Exception as e:
            self.logger.exception(e)
            self.storage.conn.commit()
            raise e

    def search(
        self,
        vector: list[float],
        k: int = 3,
        select_columns: list[str] | None = None,
        metadata_filters: dict | None = None,
        schema_data_filters: dict | None = None,
    ) -> list[dict[str, Any]]:
        """
        Return: list[{id, metadata::text, distance, select_column_0, ... , select_column_n}]
        """
        results: list[tuple] = self.storage.query_nearest_neighbours(
            vector, k, select_columns, metadata_filters, schema_data_filters
        )
        ret = []
        for row in results:
            parsed_row = {
                "id": row[0],
                "metadata": json.loads(row[1]) if row[1] is not None and row[1] != "" else None,
                "distance": row[2],
            }
            if select_columns:
                i = 3
                for col_name in select_columns:
                    parsed_row[col_name] = row[i]
                    i += 1
                if i != len(row):
                    raise AssertionError()
            ret.append(parsed_row)

        return ret

    def query(
        self,
        select_columns: list[str] | None = None,
        metadata_filters: dict | None = None,
        schema_data_filters: dict | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Get data by filter, without using vectors. By default, limit the number of output rows to 100.
        Return: list[{id, vector, metadata::text, select_column_0, ... , select_column_n}]
        """
        results = self.storage.query_by_filters(select_columns, metadata_filters, schema_data_filters, limit)
        ret = []
        for row in results:
            parsed_row = {
                "id": row[0],
                "vector": row[1],
                "metadata": json.loads(row[2]),
            }
            if select_columns:
                i = 3
                for col_name in select_columns:
                    parsed_row[col_name] = row[i]
                    i += 1
                if i != len(row):
                    raise AssertionError()
            ret.append(parsed_row)

        return ret

    def delete_vectors(
        self,
        metadata_filters: dict | None = None,
        schema_data_filters: dict | None = None,
    ):
        """Delete by filters."""
        return self.storage.delete_by_filters(
            metadata_filters=metadata_filters, schema_data_filters=schema_data_filters
        )

    def run_sql(self, sql, fetch_results=True):
        """Use this function to run complicated queries that the SDK currently doesn't support."""
        return self.storage.run_sql(sql, fetch_results=fetch_results)

    def size(self) -> int:
        """Returns the number of rows in this collection. NOTE: This function is costly. DO NOT CALL IT FREQUENTLY."""
        return self.storage.size()

    @classmethod
    def from_data(
        cls,
        table_name: str,
        ndims: int,
        vectors: list[list[float]],
        table_schema: dict[str, str] | None = None,
        metadatas: list[dict] | None = None,
        ids: list[str] | None = None,
        schema_datas: dict[str, list[str]] | None = None,
        pre_delete_table: bool = False,
        **kwargs: Any,
    ) -> HologresVector:
        if ids is None:
            ids = [str(uuid.uuid1()) for _ in vectors]

        if not metadatas:
            metadatas = [{} for _ in vectors]

        if not schema_datas:
            schema_datas = {}

        connection_string = cls.get_connection_string(kwargs)

        store = cls(
            connection_string=connection_string,
            ndims=ndims,
            table_name=table_name,
            pre_delete_table=pre_delete_table,
            table_schema=table_schema,
        )

        store.add_vectors(vectors=vectors, metadatas=metadatas, ids=ids, schema_datas=schema_datas, **kwargs)

        return store

    @classmethod
    def connection_string_from_db_params(
        cls,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ) -> str:
        """Return connection string from database parameters."""
        return f"dbname={database} user={user} password={password} host={host} port={port}"
