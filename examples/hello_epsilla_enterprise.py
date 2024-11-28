#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from pyepsilla import enterprise

# Connect to Epsilla Enterprise API EndPoint
client = enterprise.Client(base_url="https://api.epsilla.com")
client.hello()

# Get DB List
# db_list = client.get_db_list()
# print("db_list:", db_list)

db_name = "helloepsilla"
db_id = "helloepsilla-1234567890"

# Create a new db
status_code, response = client.create_db(
    db_name,
    db_id,
    min_replicas=2,
    max_replicas=2,
    sharding_init_number=3,
    sharding_capacity=1000000,
)
print(status_code, response)

# Get info of db
status_code, response = client.get_db_info(db_id)
print(status_code, response)

time.sleep(5)
# Load db
status_code, response = client.load_db(db_id)
print(status_code, response)

# Connect to an existing db
db = client.vectordb(db_id)

# Create table with schema
status_code, response = db.create_table(
    table_name="MyTable",
    table_fields=[
        {"name": "ID", "dataType": "INT", "primaryKey": True},
        {"name": "Doc", "dataType": "STRING"},
        {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4},
    ],
)
print(status_code, response)


# Insert new vector records into table
status_code, response = db.insert(
    table_name="MyTable",
    records=[
        {"ID": 11, "Doc": "Berlin", "Embedding": [0.05, 0.61, 0.76, 0.74]},
        {"ID": 12, "Doc": "London", "Embedding": [0.19, 0.81, 0.75, 0.11]},
        {"ID": 13, "Doc": "Moscow", "Embedding": [0.36, 0.55, 0.47, 0.94]},
        {"ID": 14, "Doc": "San Francisco", "Embedding": [0.18, 0.01, 0.85, 0.80]},
        {"ID": 15, "Doc": "Shanghai", "Embedding": [0.24, 0.18, 0.22, 0.44]},
    ],
)
print(status_code, response)

# Query Vectors with specific response field
status_code, response = db.query(
    table_name="MyTable",
    query_field="Embedding",
    query_vector=[0.35, 0.55, 0.47, 0.94],
    response_fields=["Doc"],
    limit=2,
)
print(status_code, response)

# Query Vectors without specific response field, then it will return all fields
status_code, response = db.query(
    table_name="MyTable",
    query_field="Embedding",
    query_vector=[0.35, 0.55, 0.47, 0.94],
    limit=2,
)
print(status_code, response)

# Get
status_code, response = db.get(
    table_name="MyTable",
    response_fields=["Doc", "Embedding"],
    filter="Doc <> 'San Francisco'",
    limit=5,
)
print(status_code, response)


# Delete specific records from table
status_code, response = db.delete(table_name="MyTable", primary_keys=[4, 5])
print(status_code, response)
status_code, response = db.delete(table_name="MyTable", filter="Doc <> 'San Francisco'")
print(status_code, response)


# Drop table
status_code, response = db.drop_table("MyTable")
print(response)

# Delete db
status_code, response = client.drop_db(db_id)
print(status_code, response)
