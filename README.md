# Epsilla Python SDK

## 1.Installation
```shell
pip3 install pyepsilla
```
or
```shell
pip3 install --upgrade pyepsilla
```

## 2.Documentation

### 2.1 Run epsilla vectordb on localhost
```shell
docker pull epsilla/vectordb
docker run -d -p 8888:8888 epsilla/vectordb
```

### 2.2 Try to use pyepsilla to connect vectordb and operate db/table

```python
from pyepsilla import vectordb

## connect to vectordb
client = vectordb.Client(
  host='localhost',
  port='8888',
  database='Default'
)

## load and use default database
client.load(name='default', path='/tmp/epsilla')
client.use(dbname="default")

## Create a table with schema in current DB
id_field = {"name": "ID", "dataType": "INT", "primaryKey": True}
doc_field = {"name": "Doc", "dataType": "STRING"}
vec_field = {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4}

fields = [id_field, doc_field, vec_field]
client.create_table(tablename="MyTable", fields=fields)
```

## 3.FAQ

https://pypi.org/project/pyepsilla/#history


