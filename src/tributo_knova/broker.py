"""Legacy provider identity and deployment defaults for the Broker v2 profile."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from tributo_broker_redis.plugin import RedisBrokerPlugin
from tributo_broker_redis.profiles.aimodel_v2.broker import (
    DRIVER_ENTRYPOINT,
    parse_broker_request,
    prepare_broker_operation,
)
from tributo_broker_redis.runtime import RedisBrokerRuntime


def _redis_broker_config(config: Mapping[str, Any]) -> dict[str, Any]:
    value = dict(config)
    if value.get("broker_id", "tributo-knova") != "tributo-knova":
        raise ValueError("broker_id must be tributo-knova")
    value["broker_id"] = "tributo-redis"
    # Only this compatibility layer supplies the historical omitted profile.
    value.setdefault("protocol", {"profile": "aimodel-v2", "protocol_version": "2.0"})
    if value["protocol"] != {"profile": "aimodel-v2", "protocol_version": "2.0"}:
        raise ValueError("tributo-knova requires the aimodel-v2 protocol profile")
    value.setdefault(
        "operations",
        {
            "training": {"execution_profiles": ["distributed"]},
            "batch_inference": {"execution_profiles": ["distributed"]},
        },
    )
    return value


class KnovaBrokerPlugin(RedisBrokerPlugin):
    """Keep the old plugin name; all protocol execution belongs to Broker."""

    broker_id = "tributo-knova"
    capabilities = RedisBrokerPlugin.capabilities.difference(
        {"operation.training.single_worker", "operation.batch_inference.single_worker"}
    )

    def validate_config(
        self, config: Mapping[str, Any], *, check_connectivity: bool = False
    ) -> None:
        super().validate_config(
            _redis_broker_config(config), check_connectivity=check_connectivity
        )

    def create_runtime(self, config: Mapping[str, Any]) -> RedisBrokerRuntime:
        return super().create_runtime(_redis_broker_config(config))


__all__ = [
    "DRIVER_ENTRYPOINT",
    "KnovaBrokerPlugin",
    "parse_broker_request",
    "prepare_broker_operation",
]
