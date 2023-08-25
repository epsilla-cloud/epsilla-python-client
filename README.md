# Epsilla Python SDK

Welcome to Python SDK for Epsilla Vector Database! 
https://pypi.org/project/pyepsilla/#history

## Installation
```shell
pip3 install pyepsilla
```
or
```shell
pip3 install --upgrade pyepsilla
```

## Documentation

### Run epsilla vectordb on localhost
```shell
docker pull epsilla/vectordb
docker run -d -p 8888:8888 epsilla/vectordb
```

### Use pyepsilla to connect to and interact with vector database

```python
from pyepsilla import vectordb

## connect to vectordb
client = vectordb.Client(
  host='localhost',
  port='8888'
)

## load and use a database
client.load_db(db_name="MyDB", db_path="/tmp/epsilla")
client.use_db(db_name="MyDB")

## create a table in the current database
client.create_table(
  table_name="MyTable",
  table_fields=[
    {"name": "ID", "dataType": "INT"},
    {"name": "Doc", "dataType": "STRING"},
    {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4}
  ]
)

## insert records
client.insert(
  table_name="MyTable",
  records=[
    {"ID": 1, "Doc": "Berlin", "Embedding": [0.05, 0.61, 0.76, 0.74]},
    {"ID": 2, "Doc": "London", "Embedding": [0.19, 0.81, 0.75, 0.11]},
    {"ID": 3, "Doc": "Moscow", "Embedding": [0.36, 0.55, 0.47, 0.94]},
    {"ID": 4, "Doc": "San Francisco", "Embedding": [0.18, 0.01, 0.85, 0.80]},
    {"ID": 5, "Doc": "Shanghai", "Embedding": [0.24, 0.18, 0.22, 0.44]}
  ]
)

## search with specific response field
status_code, response = client.query(
  table_name="MyTable",
  query_field="Embedding",
  query_vector=[0.35, 0.55, 0.47, 0.94],
  response_fields = ["Doc"],
  limit=2
)
print(response)

# search without specific response field, then it will return all fields
status_code, response = client.query(
  table_name="MyTable",
  query_field="Embedding",
  query_vector=[0.35, 0.55, 0.47, 0.94],
  limit=2
)
print(response)


## drop a table
#client.drop_table("MyTable")

## unload a database from memory
#client.unload_db("MyDB")
```

## Contributing
Bug reports and pull requests are welcome on GitHub at https://github.com/epsilla-cloud/epsilla-python-client/

If you have any question or problem, please join our discord https://discord.com/invite/cDaY2CxZc5

## We love your <a href="https://forms.gle/z73ra1sGBxH9wiUR8">Feedback</a>!

