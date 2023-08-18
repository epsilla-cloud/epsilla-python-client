#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this gist-960-euclidean benchmark example
# 1. docker run --pull=always -d -p 8888:8888 epsilla/vectordb "-r false"
# 2. pip3 install --upgrade pyepsilla
# 3. wget http://ann-benchmarks.com/gist-960-euclidean.hdf5
# 4. python3 gist-960-euclidean.py

from pyepsilla import vectordb
import h5py, datetime
from urllib.parse import urlparse

## Connect to Epsilla vector database
client = vectordb.Client(host='127.0.0.1', port='8888')
client.load_db(db_name="benchmark", db_path="/tmp/epsilla", vector_scale=1000000, wal_enabled=False) ## pay attention to change db_path to persistent volume for production environment
client.use_db(db_name="benchmark")

## Check gist-960-euclidean dataset hdf5 file to download or not
dataset_download_url = "http://ann-benchmarks.com/gist-960-euclidean.hdf5"
dataset_filename = os.path.basename(urlparse(dataset_download_url).path)
if not os.path.isfile(dataset_filename):
    os.system("wget --no-check-certificate {}".format(dataset_download_url))

## Read gist-960-euclidean data from hdf5
f = h5py.File('gist-960-euclidean.hdf5', 'r')
print(list(f.keys()))
training_data = f["train"]
size = training_data.size
records_num, dimensions = training_data.shape

## Create table for gist-960-euclidean
id_field = {"name": "id", "dataType": "INT"}
vec_field = {"name": "vector", "dataType": "VECTOR_FLOAT", "dimensions": dimensions}
fields = [id_field, vec_field]
status_code, response = client.create_table(table_name="benchmark", table_fields=fields)

## Insert 20000 data into table
# records_data = [ {"id": i, "vector": training_data[i].tolist()} for i in range(20000)]
# client.insert(table_name="benchmark", records=records_data)

## Insert all data into table
indexs = [ i for i in range(0, records_num+10000, 50000)]
print("Begin to insert all gist data into table ...")
for i in range(len(indexs)-1):
    print("-"*20)
    start=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    # print(indexs[i], indexs[i+1])
    records_data = [{"id": i, "vector": training_data[i].tolist()} for i in range(indexs[i], indexs[i+1])]
    client.insert(table_name="benchmark", records=records_data)
    end = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print("START:", start, "\nEND  :", end)

## Rebuild ann graph, it will wait until rebuild is finished, wait time is depended on the amount of dataset
client.rebuild()

## Query vectors
query_field = "vector"
query_vector = training_data[40000].tolist()
response_fields = ["id"]
limit = 2

status_code, response = client.query(table_name="benchmark", query_field=query_field, query_vector=query_vector, response_fields=response_fields, limit=limit, with_distance=True)
print("Response:", response)
