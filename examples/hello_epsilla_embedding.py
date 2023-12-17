#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example
# 1. docker run --pull=always -d -p 8888:8888 epsilla/vectordb
# 2. pip3 install --upgrade pyepsilla
# 3. python3 simple_example.py
#

from pyepsilla import vectordb

# Connect to Epsilla VectorDB
client = vectordb.Client(protocol="http", host="127.0.0.1", port="8888")

# You can also use Epsilla Cloud
# client = vectordb.Client(protocol='https', host='demo.epsilla.com', port='443')

# Load DB with path
## pay attention to change db_path to persistent volume for production environment
status_code, response = client.load_db(db_name="MyDB", db_path="/data/epsilla_demo")
print(response)

# Set DB to current DB
client.use_db(db_name="MyDB")

# Create a table with schema in current DB
status_code, response = client.create_table(
    table_name="MyTable",
    table_fields=[
        {"name": "ID", "dataType": "INT", "primaryKey": True},
        {"name": "Doc", "dataType": "STRING"},
    ],
    indices=[
      {"name": "Index", "field": "Doc"},
    ]
)
print(response)

# Get a list of table names in current DB
status_code, response = client.list_tables()
print(response)

# Insert new vector records into table
status_code, response = client.insert(
    table_name="MyTable",
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
print(response)

# Query Vectors with specific response field
status_code, response = client.query(
    table_name="MyTable",
    query_text="Where can I find a serene environment, ideal for relaxation and introspection?",
    response_fields=["Doc"],
    with_distance=True,
    limit=3
)
print(response)

# Query Vectors without specific response field, then it will return all fields
status_code, response = client.query(
    table_name="MyTable",
    query_text="Where can I find a serene environment, ideal for relaxation and introspection?",
)
print(response)

# Get Vectors
status_code, response = client.get(table_name="MyTable", limit=2)
print(response)

# status_code, response =  client.delete(table_name="MyTable", ids=[3])
status_code, response = client.delete(table_name="MyTable", primary_keys=[1, 3, 4])
# status_code, response =  client.delete(table_name="MyTable", filter="Doc <> 'San Francisco'")
print(response)


# Drop table
status_code, response = client.drop_table("MyTable")
print(response)

# Unload db
status_code, response = client.unload_db("MyDB")
print(response)
