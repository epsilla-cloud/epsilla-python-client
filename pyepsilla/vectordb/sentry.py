#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Sentry collects crash reports and performance numbers
# It is possible to turn off data collection using an environment variable named "SENTRY_DISABLE"

import os, sys, uuid, hashlib, socket, requests
import sentry_sdk
from sentry_sdk.integrations.atexit import AtexitIntegration
from .version import __version__

CONFIG_URL = "https://config.epsilla.com/candidate.json"
SENTRY_DSN = "https://08e83d2f5bffd58154ba3d377c1b7195@o4505728621412352.ingest.sentry.io/4505763445538816"

try:
    r = requests.get(CONFIG_URL, headers={"Agent": "PyEpsilla"}, timeout=2)
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
    if "SENTRY_DISABLE" not in os.environ:
        try:
            uid = hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()
            sentry_sdk.set_tag("uid", uid)
            sentry_sdk.set_tag("platform", sys.platform)
            sentry_sdk.set_tag("internal_ip", socket.gethostbyname(socket.gethostname()))
            sentry_sdk.set_tag("external_ip", get_external_ip())
            sentry_sdk.init(
                dsn=SENTRY_DSN,
                release=__version__,
                traces_sample_rate=1.0,
                integrations=[AtexitIntegration(callback=callback)],
            )

            sentry_sdk.capture_message("PyEpsilla Init at {}".format(uid), "info")
        except Exception:
            sentry_sdk.flush()
            pass
