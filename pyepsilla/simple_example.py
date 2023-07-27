#!/usr/bin/env python
# -*- coding:utf-8 -*-


## 1.Connect to Epsilla VectorDB
c = Client(host='127.0.0.1', port='8888', database='default')

##
status, body = c.welcome()
status, body = c.state()

## Load DB with path
c.load(dbname="myDB", path="/tmp/epsilla")

## Set DB to current DB
c.use(dbname="myDB")

## Unload DB
# c.unload(dbname="myDB")

## Create a table with schema in current DB
id_field = {"name": "ID", "dataType": "INT", "primaryKey": True}
doc_field = {"name": "Doc", "dataType": "STRING"}
vec_field = {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 4}

fields = [id_field, doc_field, vec_field]
c.create_table(tablename="MyTable", fields=fields)

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
c.insert(tablename="MyTable", records=records_data)

## query vector
queryField = "Embedding"
queryVector = [0.35, 0.55, 0.47, 0.94]
response = ["Doc"]
limit = 2
c.query(tablename="MyTable", queryField=queryField, queryVector=queryVector, response=response, limit=limit)

## drop table
c.drop_table("MyTable")

## drop db
c.drop_db("myDB")

