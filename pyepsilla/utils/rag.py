#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations

import json
import time
from typing import Optional

import requests


class RAG(object):
    def __init__(
        self,
        project_id: str,
        api_key: str,
        ragapp_id: str,
        conversation_id: Optional[str] = None,
    ):
        self._project_id = project_id
        self._ragapp_id = ragapp_id
        self._api_key = api_key
        self._conversation_id = conversation_id
        self._rag_base_url = "https://rag.epsilla.com"
        self._headers = {"Content-Type": "application/json", "X-API-Key": self._api_key}
        self._timeout = 15
        self._interval = 2

    def start_new_conversation(self):
        if self._conversation_id is None:
            req_url = f"{self._rag_base_url}/conversation/{self._project_id}/{self._ragapp_id}/create"
            req_data = {"summary": "summary of the conversation"}
            resp = requests.post(
                req_url,
                data=json.dumps(req_data),
                headers=self._headers,
                timeout=self._timeout,
                verify=True,
            )
            status_code = resp.status_code
            body = resp.json()
            resp.close()
            del resp

            if body["statusCode"] == 200:
                self._conversation_id = body["result"]["conversationId"]
            else:
                self._conversation_id = ""

        print(f"[INFO] current conversation id is {self._conversation_id}")

    def query(self, message: str):
        if self._conversation_id is None:
            self.start_new_conversation()

        answer = None
        contexts = None

        req_url = f"{self._rag_base_url}/chat/{self._project_id}/{self._ragapp_id}/{self._conversation_id}"
        req_data = {"message": message}
        resp = requests.post(
            req_url,
            data=json.dumps(req_data),
            headers=self._headers,
            timeout=self._timeout,
            verify=True,
        )
        status_code = resp.status_code
        body = resp.json()
        resp.close()
        del resp

        if body["statusCode"] == 200:
            time.sleep(self._interval * 4)
            req_message_id = body["result"]

            completed = False
            body = None
            while completed is not True:
                time.sleep(self._interval)
                req_url = f"{self._rag_base_url}/stream/{self._project_id}/{self._ragapp_id}/{req_message_id}"
                resp = requests.get(
                    req_url,
                    headers=self._headers,
                    timeout=self._timeout,
                    verify=True,
                )
                status_code = resp.status_code
                body = resp.json()
                resp.close()
                del resp

                completed = body["result"]["completed"]
                if completed is True:
                    break

            if body["statusCode"] == 200:
                answer = body["result"]["result"]["Generated Result"]
                contexts = [c["Content"] for c in body["result"]["result"]["knowledge"]]

            else:
                print("[ERROR] Failed to retrival answer&content from message")
        else:
            print("[ERROR] Failed to get response of the query message")

        return {"answer": answer, "contexts": contexts}


if __name__ == "__main__":
    rag = RAG(
        project_id="**********",
        api_key="eps_**********",
        ragapp_id="**********",
        conversation_id="**********",
    )

    rag.start_new_conversation()
    resp = rag.query("What's RAG?")

    print(f"[INFO] response is {resp}")
