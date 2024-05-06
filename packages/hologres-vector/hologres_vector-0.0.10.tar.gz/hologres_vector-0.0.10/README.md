# hologres-vector

[![PyPI - Version](https://img.shields.io/pypi/v/hologres-vector.svg)](https://pypi.org/project/hologres-vector)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hologres-vector.svg)](https://pypi.org/project/hologres-vector)

Use [Hologres](https://www.alibabacloud.com/product/hologres) to store large amount of vector data and perform high speed k-nearest-neighbour search!

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install hologres-vector
```

## Usage

### 输入Hologres实例连接信息

```python
from hologres_vector import HologresVector
import os

host = os.environ["HOLO_HOST"]
port = os.environ["HOLO_PORT"]
dbname = os.environ["HOLO_DBNAME"]
user = os.environ["HOLO_USER"]
password = os.environ["HOLO_PASSWORD"]

connection_string = HologresVector.connection_string_from_db_params(host, port, dbname, user, password)
```

### 与数据库建立连接并建表

建表时，需要指定向量的维数，以及表中的除向量数据、主键、json元数据以外的其他强schema列。

```python
table_name = "test_table"
holo = HologresVector(
    connection_string,     # 连接信息
    5,                     # 向量维度
    table_name=table_name, # 表名
    table_schema={"t": "text", "date": "timestamptz", "i": "int"},
    distance_method="SquaredEuclidean", # 距离函数，推荐用默认值，也可以选择"Euclidean"或"InnerProduct"
    pre_delete_table=False, # 若表已存在则先删除
)
```

### 插入向量数据与对应的其他列信息

支持强schema列 `schema_datas` 与一个json列 `metadatas`。

该接口为批量导入，内部会将输入数据切分为512行的批进行插入。

```python
vectors = [[0,0,0,0,0], [1,1,1,1,1], [2,2,2,2,2]]
ids = ['0', '1', '2'] # primary key
schema_datas = [
    {'t': 'text 0', 'date': '2023-08-02 18:30:00', 'i': 0},
    {'t': 'text 1', 'date': '2023-08-02 19:30:00', 'i': 1},
    {'t': 'text 2', 'date': '2023-08-02 20:30:00', 'i': 2},
]
metadatas = [
    {'a': "hello"},
    {'b': 123},
    {},
]

holo.upsert_vectors(vectors, ids, schema_datas=schema_datas, metadatas=metadatas)
```

### 查询

1. 普通查询：从数据库中任取一条数据（可加filter）

```python
holo.query(limit=1)
```

    [{'id': '2', 'vector': [2.0, 2.0, 2.0, 2.0, 2.0], 'metadata': {}}]

2. 近邻查询：根据向量从数据库中取最近邻

```python
holo.search([0.1, 0.1, 0.1, 0.1, 0.1], k=2, select_columns=['t'])
```

    [{'id': '0', 'metadata': {'a': 'hello'}, 'distance': 0.05, 't': 'text 0'},
    {'id': '1', 'metadata': {'b': 123}, 'distance': 4.05, 't': 'text 1'}]

3. 融合查询：根据向量从数据库中取最近邻，并用其他列查询条件约束

```python
holo.search([0.1, 0.1, 0.1, 0.1, 0.1], k=2, schema_data_filters={'t': 'text 1'})
```

    [{'id': '1', 'metadata': {'b': 123}, 'distance': 4.05}]

### 替换（upsert）

本SDK目前默认使用根据主键`id`的一种插入替换策略：当插入的数据和已有数据主键相同时，用新插入的整行替换已有的行。

```python
# 先插入一行id为3的数据
holo.upsert_vectors([[3, 3, 3, 3, 3]], [3], schema_datas=[{'t': 'old data'}])
# 再插入一行id为3的数据，下面这行会将上面的整行替换掉
holo.upsert_vectors([[-3, -3, -3, -3, -3]], [3], schema_datas=[{'t': 'new data'}])

holo.query(schema_data_filters={'id': '3'})
```

    [{'id': '3', 'vector': [-3.0, -3.0, -3.0, -3.0, -3.0], 'metadata': {}}]

### 删除

可使用与查询格式相同的filter条件来对数据进行部分删除。

```python
holo.delete_vectors(schema_data_filters={'id': '2'})
holo.query(limit=10)
```

    [{'id': '0', 'vector': [0.0, 0.0, 0.0, 0.0, 0.0], 'metadata': {'a': 'hello'}},
     {'id': '1', 'vector': [1.0, 1.0, 1.0, 1.0, 1.0], 'metadata': {'b': 123}},
     {'id': '3', 'vector': [-3.0, -3.0, -3.0, -3.0, -3.0], 'metadata': {}}]

```python
holo.delete_vectors() # 删除全部数据
```

```python
holo.query(limit=10)
```

## License

`hologres-vector` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
