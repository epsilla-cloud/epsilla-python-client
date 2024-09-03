#!/usr/bin/env python
# -*- coding:utf-8 -*-


# Question Answering Pipeline with LangChain and Epsilla
# Step1. Install the required packages
"""
pip install langchain
pip install openai
pip install tiktoken
pip install pyepsilla
pip install -U langchain-openai
pip uninstall -y langchain-community
git clone https://github.com/epsilla-cloud/langchain.git
cd ./langchain/libs/community
pip install .
"""



# Step2. Configure the OpenAI API Key
import os

os.environ["OPENAI_API_KEY"] = ""
epsilla_api_key = os.getenv("EPSILLA_API_KEY", "")
project_id = os.getenv("EPSILLA_PROJECT_ID", "")
db_id = os.getenv("EPSILLA_DB_ID", "")
db_sharding_id = os.getenv("EPSILLA_DB_SHARDING_ID", 0)

# Step3. Load the documents
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

loader = WebBaseLoader(
    "https://raw.githubusercontent.com/hwchase17/chat-your-data/master/state_of_the_union.txt"
)
documents = loader.load()
documents = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(
    documents
)
embeddings = OpenAIEmbeddings()


# Step4. Load the vector store
from langchain.vectorstores import Epsilla
from pyepsilla import cloud, vectordb


db_name = f"db_{db_id.replace('-', '_')}"
db_path = f"/data/{project_id}/{db_name}/s{db_sharding_id}"
table_name = "MyCollection"

# Connect to Epsilla Cloud
cloud_client = cloud.Client(
    project_id=project_id,
    api_key=epsilla_api_key,
)

# Connect to Vectordb
db_client = cloud_client.vectordb(db_id)

vector_store = Epsilla.from_documents(
    documents,
    embeddings,
    db_client,
    db_path=db_path,
    db_name=db_name,
    collection_name=table_name,
)

# Step4. Create the QA for Retrieval
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(), chain_type="stuff", retriever=vector_store.as_retriever()
)
query = "What did the president say about Ketanji Brown Jackson"
resp = qa.invoke(query)
print("resp:", resp)
