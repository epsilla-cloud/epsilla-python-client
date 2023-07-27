# Epsilla Python SDK

## 1.Installation
```shell
pip3 install pyepsilla
```
or
```shell
pip3 install --upgrade pyepsilla
```

## 2.Documentation

run epsilla vectordb on localhost
```shell
docker pull epsilla/vectordb
docker run -d -p 8888:8888 epsilla/vectordb
```

```python
from pyepsilla import vectordb

client = vectordb.Client(
  host='localhost',
  port='18668',
  database='Default'
)

result = client.load(name='default', path='/var/epsilla')

```

## 3.FAQ


