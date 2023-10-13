#!/usr/bin/env python
# -*- coding:utf-8 -*-

# We use PostHog to collect telemetry data for how Epsilla is used.
# Disable it by setting environment variable "POSTHOG_DISABLE"

import os, socket, platform, sys
from typing import Optional

from posthog import Posthog
from . import machineid

POSTHOG_API_KEY = "phc_HoDjIs8hJa1dHPB6dudGwCCk5Q8t3lUaAQDWzhq9DDS"
POSTHOG_HOST = "https://epsilla.ph.getmentioned.ai/ingest"

class TelemetryManager:
    """TelemetryManager is a singleton that collects telemetry data and sends it to PostHog"""

    singleton = None

    @classmethod
    def get_singleton(cls):
        if cls.singleton is None:
            cls.singleton = cls()
        return cls.singleton

    def __init__(self) -> None:
        if "POSTHOG_DISABLE" in os.environ:
            self.client = None
            return

        # We use a hashed ID to make sure telemetry data is anonymous
        try:
            self.machine_id = machineid.hashed_id("epsilla")
        except Exception:
            self.machine_id = "NA"

        self.machine_id = machineid.hashed_id("epsilla")

        self.client = Posthog(
            POSTHOG_API_KEY,
            host=POSTHOG_HOST
        )
        self.client.identify(self.machine_id, properties={"version": platform.version(), "platform": "{}-{}".format(sys.platform, platform.machine())})

        self.capture("pyepsilla initialized")

        TelemetryManager.singleton = self

    def capture(self, event: str, properties: Optional[dict] = None):
        """Capture an event and send it to PostHog"""
        if self.client is not None:
            self.client.capture(self.machine_id, event, properties=properties)
