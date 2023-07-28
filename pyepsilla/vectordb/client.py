#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json, requests

class Client():
    def __init__(self, host='localhost', port='8888', db_name='default'):
        self._protocol = "http"
        self._baseurl = "{}://{}:{}".format(self._protocol, host, port)
        self._db=db_name
        self._timeout = 5
        self._header = {'Content-type': 'application/json'}
        self._rs = requests.Session()

    def __check__(self):


    def welcome(self):
        req_url = "{}/".format(self._baseurl)
        req_data= None
        res = requests.get(url=req_url, data=json.dumps(req_data), headers=self._header, timeout=self._timeout)
        status_code = res.status_code
        body = res.text
        print("Return:", body)
        return status_code, body

    def state(self):
        req_url = "{}/state".format(self._baseurl)
        req_data= None
        res = self._rs.get(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body

    def use_db(self, db_name):
        self._db = db_name
        pass

    def load_db(self, db_name, db_path):
        req_url = "{}/api/load".format(self._baseurl)
        req_data= {"name": db_name, "path": db_path}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body

    def unload_db(self, db_name):
        req_url = "{}/api/{}/unload".format(self._baseurl, db_name)
        res = requests.post(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body

    def create_table(self, table_name="MyTable", table_fields=[]):
        req_url = "{}/api/{}/schema/tables".format(self._baseurl, self._db)
        req_data= {"name": table_name, "fields": table_fields}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body


    def insert(self, table_name="MyTable", records=[]):
        req_url = "{}/api/{}/data/insert".format(self._baseurl, self._db)
        req_data= {"table": table_name, "data": records}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body


    def query(self, table_name="MyTable", query_field="", query_vector=[], response_fields=[], limit=1):
        req_url = "{}/api/{}/data/query".format(self._baseurl, self._db)
        req_data= {"table": table_name, "queryField": query_field, "queryVector": query_vector, "response": response_fields, "limit": limit}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body


    def drop_table(self, table_name="MyTable"):
        req_url = "{}/api/{}/schema/tables/{}".format(self._baseurl, self._db, table_name)
        req_data= None
        res = requests.delete(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body

    def drop_db(self, db_name):
        req_url = "{}/api/{}/drop".format(self._baseurl, db_name)
        res = requests.delete(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body
