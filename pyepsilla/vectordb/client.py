#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json, requests

class Table():
    def __init__(self):
        pass

class DB():
    def __init__(self):
        pass

class Client():
    def __init__(self, host='localhost', port='8888', database='default'):
        self._protocol = "http"
        self._baseurl = "{}://{}:{}".format(self._protocol, host, port)
        self._db=database
        self._timeout = 5
        self._header = {'Content-type': 'application/json'}
        self._rs = requests.Session()

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

    def use(self, dbname):
        self._db = dbname
        pass

    def load(self, dbname, path):
        req_url = "{}/api/load".format(self._baseurl)
        req_data= {"path": path, "name": dbname}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body

    def unload(self, dbname):
        req_url = "{}/api/{}/unload".format(self._baseurl, dbname)
        res = requests.post(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body

    def create_table(self, tablename="MyTable", fields=[]):
        req_url = "{}/api/{}/schema/tables".format(self._baseurl, self._db)
        req_data= {"name": tablename, "fields": fields}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body


    def insert(self, tablename="MyTable", records=[]):
        req_url = "{}/api/{}/data/insert".format(self._baseurl, self._db)
        req_data= {"table": tablename, "data": records}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body


    def query(self, tablename="MyTable", queryField=[], queryVector=[], response=[], limit=1):
        req_url = "{}/api/{}/data/query".format(self._baseurl, self._db)
        req_data= {"table": tablename, "queryField": queryField, "queryVector": queryVector, "response": response, "limit": limit}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body


    def drop_table(self, tablename="MyTable"):
        req_url = "{}/api/{}/schema/tables/{}".format(self._baseurl, self._db, tablename)
        req_data= None
        res = requests.delete(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body

    def drop_db(self, dbname):
        req_url = "{}/api/{}/drop".format(self._baseurl, dbname)
        res = requests.delete(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        print("Return:", body)
        return status_code, body
