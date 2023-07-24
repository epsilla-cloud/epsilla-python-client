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

example
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


