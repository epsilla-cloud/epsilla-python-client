#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import IntEnum


class DB():
    def __init__(self):
        pass


class Table():
    def __init__(self):
        pass


class Field():
    def __init__(self, name, data_type, primary_key, dimensions, ):
        pass

class FieldType(IntEnum):
    INT1 = 1  # TINYINT
    INT2 = 2  # SMALLINT
    INT4 = 3  # INT
    INT8 = 4  # BIGINT
    FLOAT = 10
    DOUBLE = 11
    STRING = 20
    BOOL = 30
    VECTOR_FLOAT = 40
    VECTOR_DOUBLE = 41
    UNKNOWN = 999