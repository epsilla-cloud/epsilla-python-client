#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example for epsilla cloud 
# 1. create project and db on epsilla cloud
# 2. create a table with schema in db
# 3. get the api key of the project


from pyepsilla import cloud

# Connect to Epsilla Cloud
client = cloud.Client(project_id="32ef3a3f-fcb0-4c4b-98bb-fca01bca0d0a", api_key="epsilla")

# Connect to Vectordb
db = client.vectordb(db_id="df7431d0-806b-4654-8b45-4bdb20038e26")


# Create a table with schema on Epsilla Cloud Console


# Insert new vector records into table
status_code, response = db.insert(
  table_name="MyTable",
  records=[
    {"ID": 1, "Doc": "Berlin", "Embedding": [0.05, 0.61, 0.76, 0.74]},
    {"ID": 2, "Doc": "London", "Embedding": [0.19, 0.81, 0.75, 0.11]},
    {"ID": 3, "Doc": "Moscow", "Embedding": [0.36, 0.55, 0.47, 0.94]},
    {"ID": 4, "Doc": "San Francisco", "Embedding": [0.18, 0.01, 0.85, 0.80]},
    {"ID": 5, "Doc": "Shanghai", "Embedding": [0.24, 0.18, 0.22, 0.44]}
  ]
)
print(response)

# Query Vectors with specific response field, otherwise it will return all fields
status_code, response = db.query(
  table_name="MyTable",
  query_field="Embedding",
  query_vector=[0.35, 0.55, 0.47, 0.94],
  response_fields = ["Doc"],
  limit=2
)
print(response)


# Delete specific records from table
status_code, response = db.delete(
  table_name="MyTable", 
  primary_keys=[4, 5]
)
print(response)

