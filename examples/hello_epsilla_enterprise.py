#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Try this simple example for epsilla cloud enterprise
# 1. create project and db on epsilla cloud enterprise
# 2. create a table with schema in db
# 3. get the api key with project id, run this program


from pyepsilla import enterprise

# Connect to Epsilla Cloud
client = enterprise.Client(base_url="https://api-gcp-us-west1-1.epsilla.com")
client.hello()


status_code, response = client.load_db(db_name="MyDB", db_id="xxxxxx")
print(response)


