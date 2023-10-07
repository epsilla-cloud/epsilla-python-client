#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests
import socket
import datetime


class Client(Object):
    def __init__(self, projectid: str, apikey: str):
        self._project_id = project_id
        self._apikey = apikey
        self._baseurl = "https://controller.cloud.epsilla.com"
        self._db = None
        self._timeout = 10
        self._header = {'Content-type': 'application/json'}

    def welcome(self):
        req_url = "{}/".format(self._baseurl)
        req_data = None
        res = requests.get(url=req_url, data=json.dumps(req_data), headers=self._header, timeout=self._timeout)
        status_code = res.status_code
        body = res.text
        return status_code, body



    def get_all_projects(self):
        pass

    def get_project(self):
        project_id: str = self._project_id
        pass

    def get_all_dbs(self):
        project_id: str = self._project_id
        pass

    def get_db(self, db_uuid: str):
        project_id: str = self._project_id
        pass

    def create_db(self, db_uuid: str):
        pass

    def delete_db(self, db_uuid: str):
        pass

    def load_db(self, db_uuid: str):
        pass

    def unload_db(self, db_uuid: str):
        pass


    def list_tables(self):
        pass


    def create_table(self, table_name: str = "MyTable", table_fields: list[str] = None):
        pass


    def insert(self, table_name: str = "MyTable", records: list = None):
        pass

    def delete(self, table_name: str = "MyTable", ids: list[str | int] = None):
        pass

    def query(self, table_name: str = "MyTable", query_field: str = "", query_vector: list = None, response_fields: list = None, limit: int = 1, with_distance: bool = False):
        pass

    def drop_table(self, table_name: str = None):
        pass

    def drop_db(self, db_uuid: str):
        pass



