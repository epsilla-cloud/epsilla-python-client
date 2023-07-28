#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example
# 1. docker run -d -p 8888:8888 epsilla/vectordb
# 2. pip3 install --upgrade pyepsilla
# 3. python3 simple_example.py

from pyepsilla import vectordb


## 1.Connect to Epsilla VectorDB
c = vectordb.Client(host='127.0.0.1', port='8888', db_name='default')

##
status_code, response = c.welcome()
status_code, response = c.state()

## Load DB with path
status_code, response= c.load_db(db_name="myDB", db_path="/tmp/epsilla")

## Set DB to current DB
c.use_db(db_name="myDB")

## Unload DB
# c.unload(dbname="myDB")

## Create a table with schema in current DB
id_field = {"name": "ID", "dataType": "INT", "primaryKey": True}
doc_field = {"name": "Doc", "dataType": "STRING"}
vec_field = {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4}

fields = [id_field, doc_field, vec_field]
status_code, response = c.create_table(table_name="MyTable", table_fields=fields)

## Insert new vector records into table
Ids = [ i for i in range(5)]
Docs = ["Berlin", "London", "Moscow", "San Francisco", "Shanghai"]
Embedding =[[0.05, 0.61, 0.76, 0.74],
       [0.19, 0.81, 0.75, 0.11],
       [0.36, 0.55, 0.47, 0.94],
       [0.18, 0.01, 0.85, 0.80],
       [0.24, 0.18, 0.22, 0.44]
      ]

records_data = [ {"ID": i, "Doc": Docs[i], "Embedding": Embedding[i]} for i in Ids]
status_code, response = c.insert(table_name="MyTable", records=records_data)

## query vector
queryField = "Embedding"
queryVector = [0.35, 0.55, 0.47, 0.94]
response = ["Doc"]
limit = 2
status_code, response = c.query(table_name="MyTable", query_field=queryField, query_vector=queryVector, response_fields=response, limit=limit)

## drop table
status_code, response = c.drop_table("MyTable")

## drop db
status_code, response = c.drop_db("myDB")

