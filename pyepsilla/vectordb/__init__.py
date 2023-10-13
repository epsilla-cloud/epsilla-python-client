#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .client import Client
from .field import Field, FieldType
from .sentry import init_sentry
from .telemetry import TelemetryManager


init_sentry()

try: 
  telemetry_manager = TelemetryManager.get_singleton()
except Exception:
  pass
