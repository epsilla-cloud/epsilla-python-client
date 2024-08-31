# Epsilla Python SDK

Welcome to Python SDK for Epsilla Vector Database!
- <a href="https://pypi.org/project/pyepsilla/#history">Release History</a>

## Install pyepsilla
```shell
pip3 install --upgrade pyepsilla
```

## Connect to Epsilla Vector Database

#### Run epsilla vectordb on localhost
```shell
docker pull epsilla/vectordb
docker run -d -p 8888:8888 epsilla/vectordb
```

#### Use pyepsilla to connect to and interact with local vector database

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
    {"name": "ID", "dataType": "INT", "primaryKey": True},
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

## search without specific response field, then it will return all fields
status_code, response = client.query(
  table_name="MyTable",
  query_field="Embedding",
  query_vector=[0.35, 0.55, 0.47, 0.94],
  limit=2
)
print(response)

## delete records by primary_keys (and filter)
status_code, response =  client.delete(table_name="MyTable", primary_keys=[3, 4])
status_code, response =  client.delete(table_name="MyTable", filter="Doc <> 'San Francisco'")
print(response)


## drop a table
client.drop_table("MyTable")

## unload a database from memory
client.unload_db("MyDB")
```


## Connect to Epsilla Cloud

#### Register and create vectordb on Epsilla Cloud
https://cloud.epsilla.com

#### Use Epsilla Cloud module to connect with the vectordb
Please check <a href="https://github.com/epsilla-cloud/epsilla-python-client/blob/main/examples/hello_epsilla_cloud.py">example</a> for detail.
```python3
from pyepsilla import cloud

# Connect to Epsilla Cloud
client = cloud.Client(project_id="32ef3a3f-****-****-****-************", api_key="eps_**********")

# Connect to Vectordb
db = client.vectordb(db_id="df7431d0-****-****-****-************")
```


## Connect to Epsilla RAG

The resp will contains answer as well as contexts, like {"answer": "****", "contexts": ['context1','context2', ...]}

```python3
from pyepsilla import cloud

# Connect to Epsilla RAG
client = cloud.RAG(
    project_id="ce07c6fc-****-****-b7bd-b7819f22bcff",
    api_key="eps_**********",
    ragapp_id="153a5a49-****-****-b2b8-496451eda8b5",
    conversation_id="6fa22a6a-****-****-b1c3-5c795d0f45ef",
)

# Start a new conversation with RAG
client.start_new_conversation()
resp = client.query("What's RAG?")

print("[INFO] response is", resp)
```


## Contributing
Bug reports and pull requests are welcome on GitHub at [here](https://github.com/epsilla-cloud/epsilla-python-client)

If you have any question or problem, please join our [discord](https://discord.com/invite/cDaY2CxZc5)

We love your <a href="https://forms.gle/z73ra1sGBxH9wiUR8">Feedback</a>!

