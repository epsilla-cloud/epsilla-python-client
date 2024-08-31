#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Sentry collects crash reports and performance numbers
# It is possible to turn off data collection using an environment variable named "SENTRY_DISABLE"

import hashlib
import os
import platform
import socket
import sys
import uuid

import requests
import sentry_sdk
from pyepsilla.vectordb.version import __version__
from sentry_sdk.integrations.atexit import AtexitIntegration

CONFIG_URL = "https://config.epsilla.com/client.json"
SENTRY_DSN = "https://c48db3ca1d2af76b6ef5c6dd8a3efac3@o4507871625347072.ingest.us.sentry.io/4507871626985472"

try:
    r = requests.get(
        CONFIG_URL, headers={"Agent": "PyEpsilla Enterprise Client"}, timeout=2
    )
    if r.status_code == 200:
        SENTRY_DSN = r.json()["pyepsilla"][0]
except Exception:
    pass


def callback(pending, timeout):
    sys.stderr.flush()


def get_external_ip() -> str:
    try:
        return requests.get("https://api.ipify.org", timeout=2).text
    except Exception:
        return "NA"


def init_sentry():
    if os.getenv("SENTRY_DISABLE", None) is not None:
        try:
            uid = hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()
            internal_ip = socket.gethostbyname(socket.gethostname())
            external_ip = get_external_ip()
            sentry_sdk.set_tag("uid", uid)
            sentry_sdk.set_tag("internal_ip", internal_ip)
            sentry_sdk.set_tag("external_ip", external_ip)
            sentry_sdk.set_user({"ip_address": "{{auto}}"})
            sentry_sdk.set_user(
                {
                    "username": "{}-{}-{}".format(
                        socket.gethostname(), internal_ip, external_ip
                    )
                }
            )
            sentry_sdk.set_tag("version", platform.version())
            sentry_sdk.set_tag(
                "platform", "{}-{}".format(sys.platform, platform.machine())
            )
            sentry_sdk.init(
                dsn=SENTRY_DSN,
                release=__version__,
                traces_sample_rate=1.0,
                integrations=[AtexitIntegration(callback=callback)],
            )

            sentry_sdk.capture_message("PyEpsilla Enterprise Client Init", "info")
        except Exception:
            sentry_sdk.flush()
            pass
    else:
        return None
