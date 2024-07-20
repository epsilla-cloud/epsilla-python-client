#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Try this simple example for Epsilla Cloud
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
    table_name="MyTable1",
    table_fields=[
        {"name": "ID", "dataType": "INT", "primaryKey": True},
        {"name": "Doc", "dataType": "STRING"},
    ],
    indices=[
      {"name": "Index", "field": "Doc"},
    ]
)
if status_code != 200:
    raise Exception(response)
        
print(response)


# Insert new vector records into table
status_code, response = db.insert(
    table_name="MyTable1",
    records=[
        {"ID": 1, "Doc": "The garden was blooming with vibrant flowers, attracting butterflies and bees with their sweet nectar."},
        {"ID": 2, "Doc": "In the busy city streets, people rushed to and fro, hardly noticing the beauty of the day."},
        {"ID": 3, "Doc": "The library was a quiet haven, filled with the scent of old books and the soft rustling of pages."},
        {"ID": 4, "Doc": "High in the mountains, the air was crisp and clear, revealing breathtaking views of the valley below."},
        {"ID": 5, "Doc": "At the beach, children played joyfully in the sand, building castles and chasing the waves."},
        {"ID": 6, "Doc": "Deep in the forest, a deer cautiously stepped out, its ears alert for any signs of danger."},
        {"ID": 7, "Doc": "The old town's historical architecture spoke volumes about its rich cultural past."},
        {"ID": 8, "Doc": "Night fell, and the sky was a canvas of stars, shining brightly in the moon's soft glow."},
        {"ID": 9, "Doc": "A cozy cafe on the corner served the best hot chocolate, warming the hands and hearts of its visitors."},
        {"ID": 10, "Doc": "The artist's studio was cluttered but inspiring, filled with unfinished canvases and vibrant paints."},
    ],
)
if status_code != 200:
    raise Exception(response)
        
print(response)

# Query Vectors with specific response field, otherwise it will return all fields
status_code, response = db.query(
    table_name="MyTable1",
    query_text="Where can I find a serene environment, ideal for relaxation and introspection?",
)
if status_code != 200:
    raise Exception(response)
        
print(response)


# Delete specific records from table
status_code, response = db.delete(table_name="MyTable1", primary_keys=[4, 5])
if status_code != 200:
    raise Exception(response)
        
print(response)

# Delete records with filter conditions
status_code, response = db.delete(table_name="MyTable1", filter="Doc <> 'A cozy cafe on the corner served the best hot chocolate, warming the hands and hearts of its visitors.'")
if status_code != 200:
    raise Exception(response)
        
print(response)

# Drop table
status_code, response = db.drop_table(table_name="MyTable1")
if status_code != 200:
    raise Exception(response)
        
print(response)
