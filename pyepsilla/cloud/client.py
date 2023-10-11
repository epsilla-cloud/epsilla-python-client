#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests
import socket
import datetime


class Client(object):
    def __init__(self, project_id: str, api_key: str):
        self._project_id = project_id
        self._apikey = api_key
        self._baseurl = "https://dispatch.epsilla.com"

 
        self._db = None
        self._timeout = 10
        self._header = {'Content-type': 'application/json'}
    
    def vectordb(self, db_id: str):
        pass


class Vectordb(Client):
    def __init__(self, projectid: str, apikey: str, db_id: str):
        super().__init__(projectid, apikey)
        ## check projectid and apikey is valid or not
        self._check()
        ## call dispatch to get vectordb real endpoint
        self._endpoint = "{}/api/{}/vectordb".format(self._baseurl, self._project_id)

    ## insert data into table
    def insert():
        pass
    ## query data from table
    def query():
        pass
    ## delete data from table
    def delete():
        pass


    # def get_all_projects(self):
    #     pass

    # def get_project(self):
    #     project_id: str = self._project_id
    #     #return project info
    #     pass

    # def get_all_dbs(self):
    #     project_id: str = self._project_id
    #     pass

    # def get_db(self, db_uuid: str):
    #     project_id: str = self._project_id
    #     ##return db info, with public endpoint
    #     pass

    # def create_db(self, db_uuid: str):
    #     ## invoke serverless 
    #     pass

    # def delete_db(self, db_uuid: str):
    #     ## invoke serverless 
    #     pass

    # def load_db(self, db_uuid: str):
    #     pass

    # def unload_db(self, db_uuid: str):
    #     pass


    def list_tables(self):
        pass

    # def create_table(self, table_name: str = "MyTable", table_fields: list[str] = None):
    #     ## invoke serverless with schema
    #     pass


    def insert(self, table_name: str = "MyTable", records: list = None):
        requests.url = "{}/api/{}/data/insert".format(self._baseurl, self._db)
        pass

    def delete(self, table_name: str = "MyTable", ids: list[str | int] = None):
        pass

    def query(self, table_name: str = "MyTable", query_field: str = "", query_vector: list = None, response_fields: list = None, limit: int = 1, with_distance: bool = False):
        pass

    # def drop_table(self, table_name: str = None):
    #     ## invoke serverless with schema
    #     pass

    # def drop_db(self, db_uuid: str):
    #     pass



