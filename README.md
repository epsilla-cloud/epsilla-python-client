<p align="center">
    <img width="275" alt="Epsilla Logo" src="https://epsilla-misc.s3.amazonaws.com/epsilla-horizontal.png">
</p>

<p align="center">
    <b>Python Client for <a href="https://github.com/epsilla-cloud/vectordb">Epsilla</a> Vector Database</b>
</p>

<hr />

Welcome to Python SDK for Epsilla Vector Database!
- <a href="https://epsilla-inc.gitbook.io/epsilladb/vector-database/connect-to-a-database">QuickStart</a>
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

#### When Port 8888 conflicted with Jupyter Notebook
If you are using Jupyter Notebook on localhost, the port 8888 maybe conflict!

So you can change the vectordb port to another number, such as 18888
```
docker run -d -p 18888:8888 epsilla/vectordb
```

#### Use pyepsilla to connect to and interact with local vector database

```python
from pyepsilla import vectordb

db_name = "MyDB"
db_path = "/tmp/epsilla"
table_name = "MyTable"

## 1.Connect to vectordb
client = vectordb.Client(
  host='localhost',
  port='8888'
)

## 2.Load and use a database
client.load_db(db_name, db_path)
client.use_db(db_name)

## 3.Create a table in the current database
client.create_table(
  table_name=table_name,
  table_fields=[
    {"name": "ID", "dataType": "INT", "primaryKey": True},
    {"name": "Doc", "dataType": "STRING"},
    {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4}
  ]
)

## 4.Insert records
client.insert(
  table_name=table_name,
  records=[
    {"ID": 1, "Doc": "Berlin", "Embedding": [0.05, 0.61, 0.76, 0.74]},
    {"ID": 2, "Doc": "London", "Embedding": [0.19, 0.81, 0.75, 0.11]},
    {"ID": 3, "Doc": "Moscow", "Embedding": [0.36, 0.55, 0.47, 0.94]},
    {"ID": 4, "Doc": "San Francisco", "Embedding": [0.18, 0.01, 0.85, 0.80]},
    {"ID": 5, "Doc": "Shanghai", "Embedding": [0.24, 0.18, 0.22, 0.44]}
  ]
)

## 5.Search with specific response field
status_code, response = client.query(
  table_name=table_name,
  query_field="Embedding",
  query_vector=[0.35, 0.55, 0.47, 0.94],
  response_fields = ["Doc"],
  limit=2
)
print(response)

## 6.Search without specific response field, then it will return all fields
status_code, response = client.query(
  table_name=table_name,
  query_field="Embedding",
  query_vector=[0.35, 0.55, 0.47, 0.94],
  limit=2
)
print(response)

## 7.Delete records by primary_keys (and filter)
status_code, response =  client.delete(table_name=table_name, primary_keys=[3, 4])
status_code, response =  client.delete(table_name=table_name, filter="Doc <> 'San Francisco'")
print(response)


## 8.Drop a table
client.drop_table(table_name)

## 9.Unload a database from memory
client.unload_db(db_name)
```


## Connect to Epsilla Cloud

#### Register and create vectordb on Epsilla Cloud
https://cloud.epsilla.com

#### Use Epsilla Cloud module to connect with the vectordb
Please get the project_id, db_id, epsilla_api_key from Epsilla Cloud at first
```python3
from pyepsilla import cloud

epsilla_api_key = os.getenv("EPSILLA_API_KEY", "Your-Epsilla-API-Key")
project_id = os.getenv("EPSILLA_PROJECT_ID", "Your-Project-ID")
db_id = os.getenv("EPSILLA_DB_ID", "Your-DB-ID")


# 1.Connect to Epsilla Cloud
cloud_client = cloud.Client(project_id="*****-****-****-****-************", api_key="eps_**********")

# 2.Connect to Vectordb
db_client = cloud_client.vectordb(db_id)

# 3.Create a table with schema
status_code, response = db.create_table(
    table_name="MyTable",
    table_fields=[
        {"name": "ID", "dataType": "INT", "primaryKey": True},
        {"name": "Doc", "dataType": "STRING"},
        {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4},
    ],
)
print(status_code, response)

# 4.Insert new vector records into table
status_code, response = db.insert(
    table_name="MyTable",
    records=[
        {"ID": 1, "Doc": "Berlin", "Embedding": [0.05, 0.61, 0.76, 0.74]},
        {"ID": 2, "Doc": "London", "Embedding": [0.19, 0.81, 0.75, 0.11]},
        {"ID": 3, "Doc": "Moscow", "Embedding": [0.36, 0.55, 0.47, 0.94]},
        {"ID": 4, "Doc": "San Francisco", "Embedding": [0.18, 0.01, 0.85, 0.80]},
        {"ID": 5, "Doc": "Shanghai", "Embedding": [0.24, 0.18, 0.22, 0.44]},
    ],
)
print(status_code, response)


# 5.Query Vectors with specific response field, otherwise it will return all fields
status_code, response = db.query(
    table_name="MyTable",
    query_field="Embedding",
    query_vector=[0.35, 0.55, 0.47, 0.94],
    response_fields=["Doc"],
    limit=2,
)
print(status_code, response)


# 6.Delete specific records from table
status_code, response = db.delete(table_name="MyTable", primary_keys=[4, 5])
status_code, response = db.delete(table_name="MyTable", filter="Doc <> 'San Francisco'")
print(status_code, response)

# 7.Drop table
status_code, response = db.drop_table(table_name="MyTable")
print(status_code, response)


```


## Connect to Epsilla RAG
Please get the project_id, epsilla_api_key, ragapp_id, converstation_id(optional) from Epsilla Cloud at first
The resp will contains answer as well as contexts, like {"answer": "****", "contexts": ['context1','context2', ...]}

```python3
from pyepsilla import cloud

epsilla_api_key = os.getenv("EPSILLA_API_KEY", "Your-Epsilla-API-Key")
project_id = os.getenv("EPSILLA_PROJECT_ID", "Your-Project-ID")
ragapp_id = os.getenv("EPSILLA_RAGAPP_ID", "Your-RAGAPP-ID")
conversation_id = os.getenv("EPSILLA_CONVERSATION_ID", "Your-CONVERSATION-ID")

# 1.Connect to Epsilla RAG
client = cloud.RAG(
    project_id=project_id,
    api_key=epsilla_api_key,
    ragapp_id=ragapp_id,
    conversation_id=conversation_id,
)

# 2.Start a new conversation with RAG
client.start_new_conversation()
resp = client.query("What's RAG?")

print("[INFO] response is", resp)
```


## Contributing
Bug reports and pull requests are welcome on GitHub at [here](https://github.com/epsilla-cloud/epsilla-python-client)

If you have any question or problem, please join our [discord](https://discord.com/invite/cDaY2CxZc5)

We love your <a href="https://forms.gle/z73ra1sGBxH9wiUR8">Feedback</a>!

