"""Compatibility alias; implementation is owned by tributo-broker-redis."""

import sys

from tributo_broker_redis.profiles.aimodel_v2 import execution_driver as _implementation

if __name__ == "__main__":
    raise SystemExit(_implementation.main())
else:
    sys.modules[__name__] = _implementation
