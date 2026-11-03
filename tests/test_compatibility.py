"""Legacy names remain thin aliases to the Broker-owned implementation."""

import importlib

import pytest

from tributo_knova.broker import _redis_broker_config


@pytest.mark.parametrize(
    "module",
    ["protocol", "validation", "reporter", "training", "inference", "execution_driver"],
)
def test_legacy_module_is_the_broker_implementation(module):
    legacy = importlib.import_module(f"tributo_knova.{module}")
    owned = importlib.import_module(
        f"tributo_broker_redis.profiles.aimodel_v2.{module}"
    )
    assert legacy is owned


def test_legacy_config_defaults_to_v2_without_mutating_input():
    original = {"broker_id": "tributo-knova", "api_version": 1}
    result = _redis_broker_config(original)
    assert original == {"broker_id": "tributo-knova", "api_version": 1}
    assert result["broker_id"] == "tributo-redis"
    assert result["protocol"] == {"profile": "aimodel-v2", "protocol_version": "2.0"}
    assert result["operations"]["training"]["execution_profiles"] == ["distributed"]


@pytest.mark.parametrize(
    "config",
    [
        {"broker_id": "other"},
        {"protocol": {"profile": "tributo-generic-v1", "protocol_version": "1.0"}},
    ],
)
def test_legacy_entrypoint_rejects_foreign_identity_or_profile(config):
    with pytest.raises(ValueError):
        _redis_broker_config(config)
