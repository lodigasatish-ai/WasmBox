import pytest

from src.security_policy import SecurityPolicy


def test_network_access_disabled_by_default():
    policy = SecurityPolicy()

    assert policy.allow_network is False


def test_filesystem_access_disabled_by_default():
    policy = SecurityPolicy()

    assert policy.allow_filesystem is False


def test_network_access_cannot_be_enabled():
    policy = SecurityPolicy(allow_network=True)

    with pytest.raises(
        ValueError,
        match="Network access is disabled by default",
    ):
        policy.validate()


def test_filesystem_access_cannot_be_enabled():
    policy = SecurityPolicy(allow_filesystem=True)

    with pytest.raises(
        ValueError,
        match="Filesystem access is disabled by default",
    ):
        policy.validate()