#!/usr/bin/env python
# -*- coding:utf-8 -*-


from prompttools.experiment import EpsillaExperiment
from pyepsilla import vectordb
from pyepsilla.vectordb.utils import embedding_functions

emb_fns = [
    embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-MiniLM-L3-v2"),
    embedding_functions.DefaultEmbeddingFunction(),
]  # default is "all-MiniLM-L6-v2"
emb_fns_names = ["paraphrase-MiniLM-L3-v2", "default"]



# Connect to Epsilla VectorDB
epsilla_client = vectordb.Client(host='127.0.0.1', port='8888')
status_code, response = epsilla_client.load_db(db_name="vectordb", db_path="/tmp/epsilla")
epsilla_client.use_db(db_name="vectordb")

TEST_COLLECTION_NAME = "TEMPORARY_COLLECTION"
try:
    epsilla_client.drop_table(TEST_COLLECTION_NAME)
except Exception:
    pass

collection_name = TEST_COLLECTION_NAME

use_existing_collection = False  # Specify that we want to create a collection during the experiment

epsilla_client.create_table(
  table_name=collection_name,
  table_fields=[
    {"name": "documents", "dataType": "STRING"},
    {"name": "metadatas", "dataType": "JSON"},
    {"name": "ids", "dataType": "STRING"},
  ]
)



# Documents that will be added into the database
add_to_collection_params = {
    "documents": ["This is a document", "This is another document", "This is the document."],
    "metadatas": [{"source": "my_source"}, {"source": "my_source"}, {"source": "my_source"}],
    "ids": ["id1", "id2", "id3"],
}

# Our test queries
query_collection_params = {"query_texts": ["This is a query document", "This is a another query document"]}


# Set up the experiment
experiment = EpsillaExperiment(
    epsilla_client,
    collection_name,
    use_existing_collection,
    query_collection_params,
    emb_fns,
    emb_fns_names,
    add_to_collection_params,
)


experiment.run()

experiment.visualize()

