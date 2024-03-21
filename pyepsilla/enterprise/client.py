#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations

import datetime
import json
import pprint
import socket
from typing import Optional, Union

import requests
import sentry_sdk
from pydantic import BaseModel, Field, constr

from ..utils.search_engine import SearchEngine

requests.packages.urllib3.disable_warnings()  # type: ignore


from .. import cloud


class DbModel(BaseModel):
    db_name: str = Field(pattern=r"^[a-zA-Z-0-9]+$")  # constr(regex=r"^[a-zA-Z-0-9]+$")
    db_uuid: Optional[str] = None
    project_id: Optional[str] = "default"


class Client(cloud.Client):
    def __init__(
        self, base_url: str, project_id: Optional[str] = "default", headers: dict = None
    ):
        self._project_id = project_id
        self._baseurl = f"{base_url}/api/v3/project/{project_id}"
        self._timeout = 10
        self._header = {
            "Content-type": "application/json",
            "Connection": "close",
            "accept": "application/json",
        }
        if headers is not None:
            self._header.update(headers)
        self._db = None

    def hello(self):
        print("Hello Epsilla Enterprise!")

    # Get DB List
    def get_db_list(self):
        db_list = []
        req_url = "{}/vectordb/list".format(self._baseurl)
        res = requests.get(url=req_url, data=None, headers=self._header, verify=False)
        status_code = res.status_code
        body = res.json()
        if status_code == 200 and body["statusCode"] == 200:
            db_list = res.json()["result"]["uuids"]
        res.close()
        return db_list

    # Get DB Information by db_id
    def get_db_info(self, db_id: str):
        req_url = "{}/vectordb/{}".format(self._baseurl, db_id)
        res = requests.get(url=req_url, data=None, headers=self._header, verify=False)
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    # Connect to DB
    def vectordb(self, db_id: str):
        # validate db_id
        if db_id not in self.get_db_list():
            raise Exception("Invalid db_id")

        status_code, resp = self.get_db_info(db_id=db_id)
        if resp["statusCode"] == 200:
            return Vectordb(self._baseurl, db_id, self._header)
        else:
            print(resp)
            raise Exception("Failed to get db info")

    # Create DB
    def create_db(
        self,
        db_name: str = Field(pattern=r"^[a-zA-Z-0-9]{4,32}$", strict=True),
        db_id: Optional[str] = None,
        project_id: Optional[str] = "default",
        min_replicas: Optional[int] = 0,
        max_replicas: Optional[int] = 1,
        sharding_init_number: Optional[int] = 1,
        sharding_increase_step: Optional[int] = 2,
        sharding_capacity: Optional[int] = 150000,
        sharding_increase_threshold: Optional[float] = 0.9,
    ):
        req_url = "{}/vectordb/create".format(self._baseurl)
        req_data = {
            "db_name": db_name,
            "db_uuid": db_id,
            "project_id": project_id,
            "min_replicas": min_replicas,
            "max_replicas": max_replicas,
            "sharding_init_number": sharding_init_number,
            "sharding_increase_step": sharding_increase_step,
            "sharding_capacity": sharding_capacity,
            "sharding_increase_threshold": sharding_increase_threshold,
        }
        resp = requests.post(
            url=req_url,
            data=json.dumps(req_data),
            headers=self._header,
            verify=False,
        )
        status_code = resp.status_code
        body = resp.json()
        resp.close()
        return status_code, body

    # Load DB
    def load_db(self, db_id: str):
        req_url = "{}/vectordb/{}/load".format(self._baseurl, db_id)
        req_data = {}
        resp = requests.post(
            url=req_url,
            data=json.dumps(req_data),
            headers=self._header,
            verify=False,
        )
        status_code = resp.status_code
        body = resp.json()
        resp.close()
        return status_code, body

    # Unload DB
    def unload_db(self, db_id: str):
        req_url = "{}/vectordb/{}/unload".format(self._baseurl, db_id)
        req_data = {}
        resp = requests.post(
            url=req_url,
            data=json.dumps(req_data),
            headers=self._header,
            verify=False,
        )
        status_code = resp.status_code
        body = resp.json()
        resp.close()
        return status_code, body

    # Delete DB
    def drop_db(self, db_id: str):
        req_url = "{}/vectordb/{}".format(self._baseurl, db_id)
        req_data = {}
        resp = requests.delete(
            url=req_url,
            data=json.dumps(req_data),
            headers=self._header,
            verify=False,
        )
        status_code = resp.status_code
        body = resp.json()
        resp.close()
        return status_code, body


class Vectordb(object):
    def __init__(self, project_url: str, db_id: str, header: dict):
        self._db_id = db_id
        self._baseurl = "{}/vectordb/{}".format(project_url, db_id)
        self._header = header

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
        if self._db_id is None:
            raise Exception("[ERROR] db_id is None!")
        if records is None:
            records = []
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
        if self._db_id is None:
            raise Exception("[ERROR] db_id is None!")
        if records is None:
            records = []
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
        facets: Optional[list[dict]] = None,
    ):
        req_url = "{}/data/query".format(self._baseurl)
        req_data = {"table": table_name}
        if query_text is not None:
            req_data["query"] = query_text
        if query_index is not None:
            req_data["queryIndex"] = query_index
        if query_field is not None:
            req_data["queryField"] = query_field
        if query_vector is not None:
            req_data["queryVector"] = query_vector
        if response_fields is not None:
            req_data["response"] = response_fields
        if limit is not None:
            req_data["limit"] = limit
        if filter is not None:
            req_data["filter"] = filter
        if with_distance is not False:
            req_data["withDistance"] = with_distance
        if facets is not None and len(facets) > 0:
            aggregate_not_existing = 0
            for facet in facets:
                if "aggregate" not in facet:
                    aggregate_not_existing += 1
            if aggregate_not_existing > 0:
                raise Exception("[ERROR] key aggregate is a must in facets!")
            else:
                req_data["facets"] = facets

        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        del res
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
        if filter == None:
            if primary_keys == None and ids == None:
                raise Exception(
                    "[ERROR] Please provide at least one of primary keys(ids) and filter to delete record(s)."
                )
        if primary_keys == None and ids != None:
            primary_keys = ids
        if primary_keys != None and ids != None:
            try:
                sentry_sdk.sdk("Duplicate Keys with both primary keys and ids", "info")
            except Exception as e:
                pass
            print(
                "[WARN] Both primary_keys and ids are prvoided, will use primary keys by default!"
            )

        req_url = "{}/data/delete".format(self._baseurl)
        req_data = {"table": table_name}
        if primary_keys != None:
            req_data["primaryKeys"] = primary_keys
        if filter != None:
            req_data["filter"] = filter

        res = requests.post(
            url=req_url, data=json.dumps(req_data), headers=self._header, verify=False
        )
        status_code = res.status_code
        body = res.json()
        res.close()
        return status_code, body

    ## get data from table
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
        if primary_keys != None and ids != None:
            try:
                sentry_sdk.sdk("Duplicate Keys with both primary_keys and ids", "info")
            except Exception as e:
                pass
            print(
                "[WARN]Both primary_keys and ids are prvoided, will use primary keys by default!"
            )
        if primary_keys == None and ids != None:
            primary_keys = ids

        req_data = {"table": table_name}
        if response_fields != None:
            req_data["response"] = response_fields
        if primary_keys != None:
            req_data["primaryKeys"] = primary_keys
        if filter != None:
            req_data["filter"] = filter
        if skip != None:
            req_data["skip"] = skip
        if limit != None:
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
