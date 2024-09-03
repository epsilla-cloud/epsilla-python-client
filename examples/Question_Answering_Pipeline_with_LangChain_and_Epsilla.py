#!/usr/bin/env python
# -*- coding:utf-8 -*-


# Question Answering Pipeline with LangChain and Epsilla
# Step1. Install the required packages
"""
pip install langchain
pip install openai
pip install tiktoken
pip install pyepsilla
pip install -U langchain-community
pip install -U langchain-openai
"""


# Step2. Configure the OpenAI API Key
import os

os.environ["OPENAI_API_KEY"] = "*****"


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
from pyepsilla import vectordb

db_client = vectordb.Client(protocol="https", host="demo.epsilla.com", port="443")

status_code, response = db_client.load_db("MyDB", "/data/MyDB")
print(status_code, response)

vector_store = Epsilla.from_documents(
    documents,
    embeddings,
    db_client,
    db_path="/data/MyDB",
    db_name="MyDB",
    collection_name="MyCollection",
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
