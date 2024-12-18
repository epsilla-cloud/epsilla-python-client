#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example for epsilla cloud
# 1. create project and db on epsilla cloud
# 2. create a table with schema in db
# 3. get the epsilla cloud api key with project id, run this program

import os
import sys

from pyepsilla import cloud

EPSILLA_PROJECT_ID = os.getenv("EPSILLA_PROJECT_ID", "Your-Epsilla-Project-ID")
EPSILLA_API_KEY = os.getenv("EPSILLA_API_KEY", "Your-Epsilla-API-Key")

DB_ID = os.getenv("EPSILLA_DB_ID", "Your-Epsilla-DB-ID")
DB_NAME = os.getenv("DB_NAME", "MyDB")
DB_PATH = os.getenv("DB_PATH", "/tmp/epsilla_demo")
TABLE_NAME = os.getenv("TABLE_NAME", "MyTable")


if not EPSILLA_PROJECT_ID or not EPSILLA_API_KEY or not DB_ID:
    print(
        "Please set the environment variables: EPSILLA_PROJECT_ID, EPSILLA_API_KEY, EPSILLA_DB_ID"
    )
    sys.exit(1)

# Connect to Epsilla Cloud
# proxies = {"http": "127.0.0.1:1087", "https": "127.0.0.1:1087"}

cloud_client = cloud.Client(
    project_id=EPSILLA_PROJECT_ID,
    api_key=EPSILLA_API_KEY,
    # proxies=proxies
)

# Connect to Vectordb
db_client = cloud_client.vectordb(db_id=DB_ID)


try:
    # Create a table with schema
    status_code, response = db_client.create_table(
        table_name=TABLE_NAME,
        table_fields=[
            {"name": "ID", "dataType": "INT", "primaryKey": True},
            {"name": "Doc", "dataType": "STRING"},
            {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4},
        ],
    )
    print(status_code, response)
    if status_code != 200:
        raise Exception("Failed to create table")

    # Insert new vector records into table
    status_code, response = db_client.insert(
        table_name=TABLE_NAME,
        records=[
            {"ID": 1, "Doc": "Berlin", "Embedding": [0.05, 0.61, 0.76, 0.74]},
            {"ID": 2, "Doc": "London", "Embedding": [0.19, 0.81, 0.75, 0.11]},
            {"ID": 3, "Doc": "Moscow", "Embedding": [0.36, 0.55, 0.47, 0.94]},
            {"ID": 4, "Doc": "San Francisco", "Embedding": [0.18, 0.01, 0.85, 0.80]},
            {"ID": 5, "Doc": "Shanghai", "Embedding": [0.24, 0.18, 0.22, 0.44]},
        ],
    )
    print(status_code, response)
    if status_code != 200:
        raise Exception("Failed to insert records")

    # Query Vectors with specific response field, otherwise it will return all fields
    status_code, response = db_client.query(
        table_name=TABLE_NAME,
        query_field="Embedding",
        query_vector=[0.35, 0.55, 0.47, 0.94],
        response_fields=["Doc"],
        limit=2,
    )
    print(status_code, response)
    if status_code != 200:
        raise Exception("Failed to query table")

    # Delete specific records from table
    status_code, response = db_client.delete(table_name=TABLE_NAME, primary_keys=[4, 5])
    print(status_code, response)
    if status_code != 200:
        raise Exception("Failed to delete records by primary keys")

    status_code, response = db_client.delete(
        table_name=TABLE_NAME, filter="Doc <> 'San Francisco'"
    )
    print(status_code, response)
    if status_code != 200:
        raise Exception("Failed to delete records by filter")

    # Drop table
    status_code, response = db_client.drop_table(table_name=TABLE_NAME)
    print(status_code, response)
    if status_code != 200:
        raise Exception("Failed to drop table")
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
