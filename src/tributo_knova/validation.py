"""Compatibility alias; implementation is owned by tributo-broker-redis."""

import sys

from tributo_broker_redis.profiles.aimodel_v2 import validation as _implementation

sys.modules[__name__] = _implementation
