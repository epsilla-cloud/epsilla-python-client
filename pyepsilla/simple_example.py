#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example
# 1. docker run --pull=always -d -p 8888:8888 epsilla/vectordb
# 2. pip3 install --upgrade pyepsilla
# 3. python3 simple_example.py

from pyepsilla import vectordb
import random, string, time

## 1.Connect to Epsilla VectorDB
c = vectordb.Client(host='127.0.0.1', port='8888', db_name='default')
# c = vectordb.Client(host='3.209.6.179', port='8888', db_name='default')

##
status_code, response = c.welcome()
status_code, response = c.state()

## Load DB with path
status_code, response= c.load_db(db_name="myDB", db_path="/tmp/epsilla")

## Set DB to current DB
c.use_db(db_name="myDB")

## Unload DB
# c.unload(db_name="myDB")

## Create a table with schema in current DB

### define records number and vector dimension
records_num = 3000
dimensions = 8

id_field = {"name": "ID", "dataType": "INT", "primaryKey": True}
doc_field = {"name": "Doc", "dataType": "STRING"}
vec_field = {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": dimensions}

fields = [id_field, doc_field, vec_field]
status_code, response = c.create_table(table_name="MyTable", table_fields=fields)

## Insert new vector records into table
# Ids = [ i for i in range(5)]
# Docs = ["Berlin", "London", "Moscow", "San Francisco", "Shanghai"]
# Embedding =[[0.05, 0.61, 0.76, 0.74],
#        [0.19, 0.81, 0.75, 0.11],
#        [0.36, 0.55, 0.47, 0.94],
#        [0.18, 0.01, 0.85, 0.80],
#        [0.24, 0.18, 0.22, 0.44]
#       ]

## Insert new vector records
letters = list(string.ascii_lowercase+string.ascii_uppercase+string.digits)
Docs = [''.join(random.choices(letters, k=6)) for _ in range(records_num)]
Embedding = [[random.random() for _ in range(dimensions)] for _ in range(records_num)]

records_data = [ {"ID": i, "Doc": Docs[i], "Embedding": Embedding[i]} for i in range(records_num)]
status_code, response = c.insert(table_name="MyTable", records=records_data)

# time.sleep(5)
## Query Vectors
query_field = "Embedding"
query_vector = Embedding[-1]
print(Docs[-1], query_vector)
response_fields = ["Doc"]
limit = 2
status_code, response = c.query(table_name="MyTable", query_field=query_field, query_vector=query_vector, response_fields=response_fields, limit=limit)
print("status_code", status_code, "response", response)

## Drop table
#status_code, response = c.drop_table("MyTable")

## Drop db
#status_code, response = c.drop_db("myDB")

