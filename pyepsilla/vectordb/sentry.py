#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Sentry collects crash reports and performance numbers
# It is possible to turn off data collection using an environment variable named "SENTRY_OPT_OUT"

import os, sys, uuid, hashlib, requests
import sentry_sdk
from sentry_sdk.integrations.atexit import AtexitIntegration
from .version import __version__

CONFIG_URL = "https://config.epsilla.com/candidate.json"
SENTRY_DSN = "https://572e9319627537c3d25b13e4d5437ca9@o4505728621412352.ingest.sentry.io/4505728624558080"

try:
    r = requests.get(CONFIG_URL, timeout=2)
    if r.status_code == 200:
        SENTRY_DSN = r.json()["sentry"][0]
except Exception:
    pass


def filter_info(event, _hint):
    try:
        pass
    except Exception:
        pass
    return event

def callback(pending, timeout):
    sys.stderr.flush()

def init_sentry():
    if "SENTRY_OPT_OUT" not in os.environ:
        try:
            sentry_sdk.init(
                dsn=SENTRY_DSN,
                release=__version__,
                traces_sample_rate=1.0,
                include_local_variables=True,
                send_default_pii=True,
                attach_stacktrace=True,
                before_send=filter_info,
                include_source_context=True,
                debug=False,
                integrations=[AtexitIntegration(callback=callback)],
            )
            uuid = hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()
            sentry_sdk.capture_message("PyEpsilla Init at {}".format(uuid), "info")
        except Exception:
            sentry_sdk.flush()
            pass
