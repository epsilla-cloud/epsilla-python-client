#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json, requests, socket

class Client():
    def __init__(self, protocol = 'http', host='localhost', port='8888'):
        self._protocol = protocol
        self._host = host
        self._port = port
        self._baseurl = "{}://{}:{}".format(self._protocol, self._host, self._port)
        self._db=None
        self._timeout = 10
        self._header = {'Content-type': 'application/json'}
        self.check_networking()

    def check_networking(self):
        socket.setdefaulttimeout(self._timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        check_result = s.connect_ex((self._host, int(self._port)))
        s.close()
        if check_result == 0:
            print("[INFO] Connected to {}:{} successfully.".format(self._host, self._port))
        else:
            raise Exception("[ERROR] Failed to connect to {}:{}".format(self._host, self._port))

    def welcome(self):
        req_url = "{}/".format(self._baseurl)
        req_data= None
        res = requests.get(url=req_url, data=json.dumps(req_data), headers=self._header, timeout=self._timeout)
        status_code = res.status_code
        body = res.text
        return status_code, body

    def state(self):
        req_url = "{}/state".format(self._baseurl)
        req_data= None
        res = requests.get(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body

    def use_db(self, db_name):
        self._db = db_name

    def load_db(self, db_name, db_path, vector_scale=None):
        req_url = "{}/api/load".format(self._baseurl)
        req_data= {"name": db_name, "path": db_path}
        if vector_scale is not None:
            req_data["vectorScale"] = vector_scale
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body

    def unload_db(self, db_name):
        req_url = "{}/api/{}/unload".format(self._baseurl, db_name)
        res = requests.post(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body

    def create_table(self, table_name="MyTable", table_fields=[]):
        if self._db is None:
            raise Exception("[ERROR] Please use_db() first!")
        req_url = "{}/api/{}/schema/tables".format(self._baseurl, self._db)
        req_data= {"name": table_name, "fields": table_fields}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body


    def insert(self, table_name="MyTable", records=[]):
        if self._db is None:
            raise Exception("[ERROR] Please use_db() first!")
        req_url = "{}/api/{}/data/insert".format(self._baseurl, self._db)
        req_data= {"table": table_name, "data": records}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body


    def query(self, table_name="MyTable", query_field="", query_vector=[], response_fields=[], limit=1):
        if self._db is None:
            raise Exception("[ERROR] Please use_db() first!")
        req_url = "{}/api/{}/data/query".format(self._baseurl, self._db)
        req_data= {"table": table_name, "queryField": query_field, "queryVector": query_vector, "response": response_fields, "limit": limit}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body


    def drop_table(self, table_name="MyTable"):
        if self._db is None:
            raise Exception("[ERROR] Please use_db() first!")
        req_url = "{}/api/{}/schema/tables/{}".format(self._baseurl, self._db, table_name)
        req_data= None
        res = requests.delete(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body

    def drop_db(self, db_name):
        req_url = "{}/api/{}/drop".format(self._baseurl, db_name)
        res = requests.delete(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body
