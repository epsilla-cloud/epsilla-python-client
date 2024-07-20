#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Try this simple example for epsilla cloud
    Step 1: Create project and db on Epsilla Cloud
    Step 2: Create a table with schema in db
    Step 3: Get the API key with project id, run this program
"""

import sys
import os
from pyepsilla import cloud
from dotenv import load_dotenv, find_dotenv

# Import the keys from .env file
load_dotenv(find_dotenv())
PROJECT_ID = os.getenv("PROJECT_ID")
EPSILLA_CLOUD_API_KEY = os.getenv("EPSILLA_CLOUD_API_KEY")
DB_ID = os.getenv("DB_ID")

try:
    # Connect to Epsilla Cloud
    client = cloud.Client(
        project_id=PROJECT_ID,
        api_key=EPSILLA_CLOUD_API_KEY,
    )

    # Connect to Vectordb
    db = client.vectordb(db_id=DB_ID)
    
except Exception as e:
    print(f"Failed to connect to Epsilla Cloud: {e}")


# Create a table with schema
status_code, response = db.create_table(
    table_name="MyTable",
    table_fields=[
        {"name": "ID", "dataType": "INT", "primaryKey": True},
        {"name": "Doc", "dataType": "STRING"},
        {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4},
    ],
)
if status_code != 200:
    raise Exception(response)
        
print(response)


# Insert new vector records into table
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
if status_code != 200:
    raise Exception(response)
        
print(response)

# Query Vectors with specific response field, otherwise it will return all fields
status_code, response = db.query(
    table_name="MyTable",
    query_field="Embedding",
    query_vector=[0.35, 0.55, 0.47, 0.94],
    response_fields=["Doc"],
    limit=2,
)
if status_code != 200:
    raise Exception(response)
        
print(response)


# Delete specific records from 
status_code, response = db.delete(table_name="MyTable", primary_keys=[4, 5])
if status_code != 200:
    raise Exception(response)
        
print(response)

# Delete records with filter conditions
status_code, response = db.delete(table_name="MyTable", filter="Doc <> 'San Francisco'")
if status_code != 200:
    raise Exception(response)
        
print(response)

# Drop table
# This never works either through code or GUI
status_code, response = db.drop_table(table_name="MyTable")
if status_code != 200:
    raise Exception(response)
        
print(response)