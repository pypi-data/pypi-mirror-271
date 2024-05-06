import logging
import os
import uuid

import pytest

from hologres_vector import HologresVector

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_connection_string():
    host = os.environ["HOLO_HOST"]
    port = os.environ["HOLO_PORT"]
    dbname = os.environ["HOLO_DBNAME"]
    user = os.environ["HOLO_USER"]
    password = os.environ["HOLO_PASSWORD"]

    return HologresVector.connection_string_from_db_params(host, port, dbname, user, password)


def test_connection():
    table_name = "test_vector_table_" + uuid.uuid1().hex

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema={"t": "text", "date": "timestamptz", "i": "int"},
        pre_delete_table=True,
        logger=logger,
    )

    res = holo.run_sql(
        f"select count(1) from hologres.hg_table_properties "
        f"where table_name = '{table_name}' and property_key = 'table_id'"
    )
    assert res[0][0] == 1
    holo.run_sql(f"drop table {table_name}", False)


def normalize(v):
    # 计算向量的欧几里得范数(L2范数)
    norm = sum(x**2 for x in v) ** 0.5
    # 避免除以0
    if norm == 0:
        return v
    # 归一化向量
    return [x / norm for x in v]


def insert_example_data(
    holo: HologresVector, use_metadata: bool = False, use_id: bool = False, do_normalize: bool = False
):
    vectors = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
    if do_normalize:
        vectors = [normalize(v) for v in vectors]
    schema_datas = [
        {"t": "text 0", "date": "2023-08-02 13:00:00", "i": 0},
        {"t": "text 1", "date": "2023-08-02 14:00:00", "i": 1},
        {"t": "text 2", "date": "2023-08-02 15:00:00", "i": 2},
    ]
    metadatas = None
    if use_metadata:
        metadatas = schema_datas

    ids = None
    if use_id:
        ids = [0, 1, 2]

    holo.upsert_vectors(vectors, ids=ids, metadatas=metadatas, schema_datas=schema_datas)


def test_insert():
    table_name = "test_vector_table_" + uuid.uuid1().hex

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema={"t": "text", "date": "timestamptz", "i": "int"},
        pre_delete_table=True,
        logger=logger,
    )

    insert_example_data(holo)

    res = holo.run_sql(f"select vector, t, date, i, metadata from {table_name} order by i")
    assert len(res) == 3
    for i in range(3):
        assert res[i][1] == f"text {i}"
        assert res[i][3] == i
        assert res[i][4] == {}

    holo.run_sql(f"drop table {table_name}", False)


def test_upsert():
    table_name = "test_vector_table_" + uuid.uuid1().hex

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema={"t": "text", "date": "timestamptz", "i": "int"},
        pre_delete_table=True,
        logger=logger,
    )

    insert_example_data(holo, use_metadata=False, use_id=True)

    res = holo.run_sql(f"select vector, t, date, i, metadata from {table_name} order by i")
    assert len(res) == 3
    for i in range(3):
        assert res[i][1] == f"text {i}"
        assert res[i][3] == i
        assert res[i][4] == {}

    # insert again with metadata
    insert_example_data(holo, use_metadata=True, use_id=True)
    res = holo.run_sql(f"select vector, t, date, i, metadata from {table_name} order by i")
    assert len(res) == 3
    for i in range(3):
        assert res[i][1] == f"text {i}"
        assert res[i][3] == i
        assert res[i][4]["i"] == i

    holo.run_sql(f"drop table {table_name}", False)


def test_search():
    table_name = "test_vector_table_" + uuid.uuid1().hex

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema={"t": "text", "date": "timestamptz", "i": "int"},
        pre_delete_table=True,
        logger=logger,
    )
    insert_example_data(holo)

    res = holo.search([2, 2, 2, 2, 2], k=2, select_columns=["t", "date", "i"])
    assert len(res) == 2
    for i in range(2):
        assert res[i]["i"] == i
        assert res[i]["t"] == f"text {i}"

    holo.run_sql(f"drop table {table_name}", False)


def test_reconnect():
    table_name = "test_vector_table_" + uuid.uuid1().hex
    table_schema = {"t": "text", "date": "timestamptz", "i": "int"}

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema=table_schema,
        pre_delete_table=True,
        logger=logger,
    )
    insert_example_data(holo)

    holo = None  # close connection

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema=table_schema,
        logger=logger,
    )

    res = holo.search([2, 2, 2, 2, 2], k=2, select_columns=["t", "date", "i"])
    assert len(res) == 2
    for i in range(2):
        assert res[i]["i"] == i
        assert res[i]["t"] == f"text {i}"

    holo.run_sql(f"drop table {table_name}", False)


def test_metadata_filter():
    table_name = "test_vector_table_" + uuid.uuid1().hex
    table_schema = {"t": "text", "date": "timestamptz", "i": "int"}

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema=table_schema,
        pre_delete_table=True,
        logger=logger,
    )
    insert_example_data(holo, use_metadata=True)

    res = holo.search([2, 2, 2, 2, 2], k=2, select_columns=["i"], metadata_filters={"t": "text 1"})
    assert len(res) == 1
    assert res[0]["i"] == 1

    holo.run_sql(f"drop table {table_name}", False)


def test_schema_data_filter():
    table_name = "test_vector_table_" + uuid.uuid1().hex
    table_schema = {"t": "text", "date": "timestamptz", "i": "int"}

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema=table_schema,
        pre_delete_table=True,
        logger=logger,
    )
    insert_example_data(holo)

    res = holo.search([2, 2, 2, 2, 2], k=2, select_columns=["i"], schema_data_filters={"t": "text 1"})
    assert len(res) == 1
    assert res[0]["i"] == 1

    holo.run_sql(f"drop table {table_name}", False)


def test_delete():
    table_name = "test_vector_table_" + uuid.uuid1().hex
    table_schema = {"t": "text", "date": "timestamptz", "i": "int"}

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema=table_schema,
        pre_delete_table=True,
        logger=logger,
    )

    insert_example_data(holo, use_metadata=True)
    res = holo.run_sql(f"select count(1), sum(i) from {table_name}")
    assert res[0][0] == 3
    assert res[0][1] == 3
    assert holo.size() == 3

    holo.delete_vectors(schema_data_filters={"t": "text 0"})
    res = holo.run_sql(f"select count(1), sum(i) from {table_name}")
    assert res[0][0] == 2
    assert res[0][1] == 3
    assert holo.size() == 2

    holo.delete_vectors(metadata_filters={"t": "text 1"})
    res = holo.run_sql(f"select count(1), sum(i) from {table_name}")
    assert res[0][0] == 1
    assert res[0][1] == 2
    assert holo.size() == 1

    holo.delete_vectors()
    res = holo.run_sql(f"select count(1) from {table_name}")
    assert res[0][0] == 0
    assert holo.size() == 0

    holo.run_sql(f"drop table {table_name}", False)


@pytest.mark.parametrize("distance_method", ["SquaredEuclidean", "Euclidean", "InnerProduct"])
def test_distance_method(distance_method):
    table_name = "test_vector_table_" + uuid.uuid1().hex

    holo = HologresVector(
        get_connection_string(),
        5,
        table_name=table_name,
        table_schema={"t": "text", "date": "timestamptz", "i": "int"},
        distance_method=distance_method,
        pre_delete_table=True,
        logger=logger,
    )
    insert_example_data(holo, do_normalize=True)

    res = holo.search(normalize([0, 1, 2, 3, 4]), k=2, select_columns=["t", "date", "i"])
    assert len(res) == 2
    for i in range(2):
        assert res[i]["i"] == i
        assert res[i]["t"] == f"text {i}"

    holo.run_sql(f"drop table {table_name}", False)
