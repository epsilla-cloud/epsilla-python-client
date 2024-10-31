#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example for epsilla rag
# 1. create client to connect to epsilla rag
# 2. launch a new converstation with epsilla rag
# 3. send a query and wait the response from epsilla ragg

from pyepsilla import cloud

# Connect to Epsilla RAG, conversation_id is not a must
client = cloud.RAG(
    project_id="**********",
    api_key="eps_**********",
    ragapp_id="**********",
    conversation_id="**********",
)

# Start a new conversation with RAG
client.start_new_conversation()
resp = client.query("What's RAG?")

print(f"[INFO] response is {resp}")
