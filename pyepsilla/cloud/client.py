#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json, datetime, socket, requests, json, pprint


class Client(object):
    def __init__(self, project_id: str, api_key: str):
        self._project_id = project_id
        self._apikey = api_key
        self._baseurl = "https://dispatch.epsilla.com/api/v2/project/{}".format(self._project_id)
        self._timeout = 10
        self._header = {'Content-type': 'application/json', 'X-API-Key': api_key}


    def validate(self):
        res = requests.get(url=self._baseurl, data=None, headers=self._header)
        return res.json()


    def get_db_list(self):
        db_list = []
        req_url = "{}/vectordb/list".format(self._baseurl)
        res = requests.get(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        if status_code == 200 and body["statusCode"] == 200:
            db_list = [ db_id for db_id in res.json()["result"] ]
        return db_list


    def get_db_info(self, db_id: str):
        req_url = "{}/vectordb/{}".format(self._baseurl, db_id)
        res = requests.get(url=req_url, data=None, headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body


    def vectordb(self, db_id: str):
        ## validate project_id and api_key
        res = self.validate()
        if res["statusCode"] != 200:
            if res["statusCode"] == 404:
                raise Exception("Invalid project_id")
            if res["statusCode"] == 401:
                raise Exception("Invalid api_key")

        ## validate db_id
        if not db_id in self.get_db_list():
            raise Exception("Invalid db_id")
        
        ## fetch db public endpoint
        status_code, resp = self.get_db_info(db_id=db_id)
        if resp["statusCode"] == 200:
            return Vectordb(self._project_id, db_id, self._apikey, resp["result"]["public_endpoint"])
        else:
            print(resp)
            raise Exception("Failed to get db info")
    
    ## TODO
    def create_db(self, db_id: str, db_type: str, db_name: str, db_description: str = ""):
        pass

    def delete_db(self, db_id: str):
        pass



class Vectordb(Client):
    def __init__(self, project_id: str, db_id: str, api_key: str, public_endpoint: str):
        self._project_id = project_id
        self._db_id = db_id
        self._api_key = api_key
        self._public_endpoint = public_endpoint
        self._baseurl = "https://{}/api/v2/project/{}/vectordb/{}".format(self._public_endpoint, self._project_id, self._db_id)
        self._header = {'Content-type': 'application/json', 'X-API-Key': self._api_key}


    ## TODO
    ## create table
    def create_table(self, table_name: str = "MyTable", table_fields: list[str] = None):
        pass

    ## drop table
    def drop_table(self, table_name: str):
        pass


    ## insert data into table
    def insert(self, table_name: str, records: list[dict]):
        req_url = "{}/data/insert".format(self._baseurl)
        req_data = {"table": table_name, "data": records}
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body


    ## query data from table
    def query(self, table_name: str, query_field: str = "", query_vector: list = None, response_fields: list = None, limit: int = 1, with_distance: bool = False):
        req_url = "{}/data/query".format(self._baseurl)
        req_data = {
            "table": table_name,
            "queryField": query_field,
            "queryVector": query_vector,
            "response": response_fields,
            "limit": limit,
            "withDistance": with_distance
        }
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body


    ## delete data from table
    def delete(self, table_name: str, primary_keys: list[str | int] = None):
        req_url = "{}/data/delete".format(self._baseurl)
        req_data = {
            "table": table_name,
            "primaryKeys": primary_keys
        }
        res = requests.post(url=req_url, data=json.dumps(req_data), headers=self._header)
        status_code = res.status_code
        body = res.json()
        return status_code, body



