import pytest

from src.security_policy import SecurityPolicy


def test_filesystem_is_disabled_by_default():
    policy = SecurityPolicy()

    assert policy.allow_filesystem is False


def test_network_is_disabled_by_default():
    policy = SecurityPolicy()

    assert policy.allow_network is False


def test_filesystem_access_cannot_be_enabled():
    with pytest.raises(ValueError, match="Filesystem access"):
        SecurityPolicy(allow_filesystem=True).validate()


def test_network_access_cannot_be_enabled():
    with pytest.raises(ValueError, match="Network access"):
        SecurityPolicy(allow_network=True).validate()