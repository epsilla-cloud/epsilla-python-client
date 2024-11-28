#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example for epsilla cloud
# 1. create project and db on epsilla cloud
# 2. create a table with schema in db
# 3. get the api key with project id, run this program

import sys

from pyepsilla import cloud

# Connect to Epsilla Cloud
client = cloud.Client(
    project_id="7a68814c-f839-4a67-9ec6-93c027c865e6",
    api_key="epsilla-cloud-api-key",
)

# Connect to Vectordb
db = client.vectordb(db_id="6accafb1-476d-43b0-aa64-12ebfbf7442d")


# Create a table with schema
status_code, response = db.create_table(
    table_name="MyTable",
    table_fields=[
        {"name": "ID", "dataType": "INT", "primaryKey": True},
        {"name": "Doc", "dataType": "STRING"},
    ],
    indices=[
        {"name": "Index", "field": "Doc"},
    ],
)
print(status_code, response)


# Insert new vector records into table
status_code, response = db.insert(
    table_name="MyTable",
    records=[
        {
            "ID": 1,
            "Doc": "The garden was blooming with vibrant flowers, attracting butterflies and bees with their sweet nectar.",
        },
        {
            "ID": 2,
            "Doc": "In the busy city streets, people rushed to and fro, hardly noticing the beauty of the day.",
        },
        {
            "ID": 3,
            "Doc": "The library was a quiet haven, filled with the scent of old books and the soft rustling of pages.",
        },
        {
            "ID": 4,
            "Doc": "High in the mountains, the air was crisp and clear, revealing breathtaking views of the valley below.",
        },
        {
            "ID": 5,
            "Doc": "At the beach, children played joyfully in the sand, building castles and chasing the waves.",
        },
        {
            "ID": 6,
            "Doc": "Deep in the forest, a deer cautiously stepped out, its ears alert for any signs of danger.",
        },
        {
            "ID": 7,
            "Doc": "The old town's historical architecture spoke volumes about its rich cultural past.",
        },
        {
            "ID": 8,
            "Doc": "Night fell, and the sky was a canvas of stars, shining brightly in the moon's soft glow.",
        },
        {
            "ID": 9,
            "Doc": "A cozy cafe on the corner served the best hot chocolate, warming the hands and hearts of its visitors.",
        },
        {
            "ID": 10,
            "Doc": "The artist's studio was cluttered but inspiring, filled with unfinished canvases and vibrant paints.",
        },
    ],
)
print(status_code, response)

# Query Vectors with specific response field, otherwise it will return all fields
status_code, response = db.query(
    table_name="MyTable",
    query_text="Where can I find a serene environment, ideal for relaxation and introspection?",
)
print(status_code, response)


# Delete specific records from table
status_code, response = db.delete(table_name="MyTable", primary_keys=[4, 5])
status_code, response = db.delete(
    table_name="MyTable",
    filter="Doc <> 'A cozy cafe on the corner served the best hot chocolate, warming the hands and hearts of its visitors.'",
)
print(status_code, response)

# Drop table
status_code, response = db.drop_table(table_name="MyTable")
print(status_code, response)
