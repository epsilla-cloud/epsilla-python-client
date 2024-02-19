#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations

import datetime
import json
import pprint
import socket
from typing import Optional, Union
from ..utils.search_engine import SearchEngine

import requests
import sentry_sdk
from pydantic import BaseModel, Field, constr

requests.packages.urllib3.disable_warnings()


class Client(object):
    def __init__(self, project_id: str, api_key: str, headers: dict = None):
        self._project_id = project_id
        self._apikey = api_key
        self._baseurl = "https://dispatch.epsilla.com/api/v3/project/{}".format(
            self._project_id
        )
        self._timeout = 10
        self._header = {
            "Content-type": "application/json",
            "Connection": "close",
            "X-API-Key": api_key,
        }
        if headers is not None:
            self._header.update(headers)

    def validate(self):
        res = requests.get(
            url=self._baseurl + "/vectordb/list",
            data=None,
            headers=self._header,
            verify=False,
        )
        data = res.json()
        res.close()
        return data

    def get_db_list(self):
        db_list = []
        req_url = "{}/vectordb/list".format(self._baseurl)
        res = requests.get(url=req_url, data=None, headers=self._header, verify=False)
        status_code = res.status_code
        body = res.json()
        if status_code == 200 and body["statusCode"] == 200:
            db_list = [db_id for db_id in res.json()["result"]]
        res.close()
        return db_list

    def get_db_info(self, db_id: str):
        req_url = "{}/vectordb/{}".format(self._baseurl, db_id)
        res = requests.get(url=req_url, data=None, headers=self._header, verify=False)
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    def get_db_statistics(self, db_id: str):
        req_url = "{}/vectordb/{}/statistics".format(self._baseurl, db_id)
        req_data = None
        res = requests.get(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    def vectordb(self, db_id: str):
        # validate project_id and api_key
        res = self.validate()
        if res["statusCode"] != 200:
            if res["statusCode"] == 404:
                raise Exception("Invalid project_id")
            if res["statusCode"] == 401:
                raise Exception("Invalid api_key")

        # validate db_id
        db_list = self.get_db_list()
        if db_id not in db_list:
            raise Exception("Invalid db_id")

        # fetch db public endpoint
        status_code, resp = self.get_db_info(db_id=db_id)
        if resp["statusCode"] == 200:
            return Vectordb(
                self._project_id, db_id, self._apikey, resp["result"]["public_endpoint"]
            )
        else:
            print(resp)
            raise Exception("Failed to get db info")


class Vectordb(Client):
    def __init__(
        self,
        project_id: str,
        db_id: str,
        api_key: str,
        public_endpoint: str,
        headers: dict = None,
    ):
        self._project_id = project_id
        self._db_id = db_id
        self._api_key = api_key
        self._public_endpoint = public_endpoint
        self._baseurl = "https://{}/api/v3/project/{}/vectordb/{}".format(
            self._public_endpoint, self._project_id, self._db_id
        )
        self._header = {"Content-type": "application/json", "X-API-Key": self._api_key}
        if headers is not None:
            self._header.update(headers)

    # List table
    def list_tables(self):
        if self._db_id is None:
            raise Exception("[ERROR] db_id is None!")
        req_url = "{}/table/list".format(self._baseurl)
        res = requests.get(url=req_url, headers=self._header, verify=False)
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    # Create table
    def create_table(
        self,
        table_name: str,
        table_fields: list[dict] = None,
        indices: list[dict] = None,
    ):
        if self._db_id is None:
            raise Exception("[ERROR] db_id is None!")
        if table_fields is None:
            table_fields = []
        req_url = "{}/table/create".format(self._baseurl)
        req_data = {"name": table_name, "fields": table_fields}
        if indices is not None:
            req_data["indices"] = indices
        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    # Drop table
    def drop_table(self, table_name: str):
        if self._db_id is None:
            raise Exception("[ERROR] db_id is None!")
        req_url = "{}/table/delete?table_name={}".format(self._baseurl, table_name)
        req_data = {}
        res = requests.delete(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    # Insert data into table
    def insert(self, table_name: str, records: list[dict]):
        req_url = "{}/data/insert".format(self._baseurl)
        req_data = {"table": table_name, "data": records}
        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    def upsert(self, table_name: str, records: list[dict]):
        req_url = "{}/data/insert".format(self._baseurl)
        req_data = {"table": table_name, "data": records, "upsert": True}
        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    # Query data from table
    def query(
        self,
        table_name: str,
        query_text: str = None,
        query_index: str = None,
        query_field: str = None,
        query_vector: Union[list, dict] = None,
        response_fields: Optional[list] = None,
        limit: int = 2,
        filter: Optional[str] = None,
        with_distance: Optional[bool] = False,
    ):
        req_url = "{}/data/query".format(self._baseurl)
        req_data = {"table": table_name}
        if query_text is not None:
            req_data["query"] = query_text
        if query_index is not None:
            req_data["queryIndex"] = query_index
        if query_field != None:
            req_data["queryField"] = query_field
        if query_vector != None:
            req_data["queryVector"] = query_vector
        if response_fields != None:
            req_data["response"] = response_fields
        if limit != None:
            req_data["limit"] = limit
        if filter != None:
            req_data["filter"] = filter
        if with_distance != None:
            req_data["withDistance"] = with_distance

        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    # Delete data from table
    def delete(
        self,
        table_name: str,
        primary_keys: Optional[list[Union[str, int]]] = None,
        ids: Optional[list[Union[str, int]]] = None,
        filter: Optional[str] = None,
    ):
        """Epsilla supports delete records by primary keys as default for now."""
        if filter is None:
            if primary_keys is None and ids is None:
                raise Exception(
                    "[ERROR] Please provide at least one of primary keys(ids) and filter to delete record(s)."
                )
        if primary_keys is None and ids is not None:
            primary_keys = ids
        if primary_keys is not None and ids is not None:
            try:
                sentry_sdk.sdk("Duplicate Keys with both primary keys and ids", "info")
            except Exception as e:
                pass
            print(
                "[WARN] Both primary_keys and ids are prvoided, will use primary keys by default!"
            )

        req_url = "{}/data/delete".format(self._baseurl)
        req_data = {"table": table_name}
        if primary_keys is not None:
            req_data["primaryKeys"] = primary_keys
        if filter is not None:
            req_data["filter"] = filter

        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    # Get data from table
    def get(
        self,
        table_name: str,
        response_fields: Optional[list] = None,
        primary_keys: Optional[list[Union[str, int]]] = None,
        ids: Optional[list[Union[str, int]]] = None,
        filter: Optional[str] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """Epsilla supports get records by primary keys as default for now."""
        if primary_keys is not None and ids is not None:
            try:
                sentry_sdk.sdk("Duplicate Keys with both primary_keys and ids", "info")
            except Exception as e:
                pass
            print(
                "[WARN]Both primary_keys and ids are prvoided, will use primary keys by default!"
            )
        if primary_keys is None and ids is not None:
            primary_keys = ids

        req_data = {"table": table_name}
        if response_fields is not None:
            req_data["response"] = response_fields
        if primary_keys is not None:
            req_data["primaryKeys"] = primary_keys
        if filter is not None:
            req_data["filter"] = filter
        if skip is not None:
            req_data["skip"] = skip
        if limit is not None:
            req_data["limit"] = limit

        req_url = "{}/data/get".format(self._baseurl)
        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    def as_search_engine(self):
        return SearchEngine(self)
