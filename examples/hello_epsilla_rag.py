#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example for epsilla rag
# 1. create client to connect to epsilla rag
# 2. launch a new converstation with epsilla rag
# 3. send a query and wait the response from epsilla ragg

import os

from pyepsilla import cloud

EPSILLA_PROJECT_ID = os.getenv("EPSILLA_PROJECT_ID", "Your-Epsilla-Project-ID")
EPSILLA_API_KEY = os.getenv("EPSILLA_API_KEY", "Your-Epsilla-API-Key")
EPSILLA_RAGAPP_ID = os.getenv("EPSILLA_RAGAPP_ID", "Your-Epsilla-RAGAPP-ID")
EPSILLA_CONVERSATION_ID = os.getenv("EPSILLA_CONVERSATION_ID", None)


# Connect to Epsilla RAG, conversation_id is not a must
client = cloud.RAG(
    project_id=EPSILLA_PROJECT_ID,
    api_key=EPSILLA_API_KEY,
    ragapp_id=EPSILLA_RAGAPP_ID,
    conversation_id=EPSILLA_CONVERSATION_ID,
)

# Start a new conversation with RAG
client.start_new_conversation()
resp = client.query("What's RAG?")

print(f"[INFO] response is {resp}")
