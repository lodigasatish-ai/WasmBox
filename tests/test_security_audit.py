from src.security_audit import SecurityAuditResult, audit_security_policy
from src.security_policy import SecurityPolicy


def test_security_audit_passes_for_valid_policy():
    policy = SecurityPolicy()

    result = audit_security_policy(policy)

    assert isinstance(result, SecurityAuditResult)
    assert result.passed is True
    assert "security policy validation" in result.checks
    assert "filesystem access disabled" in result.checks
    assert "network access disabled" in result.checks
    assert result.failures == []


def test_security_audit_fails_for_invalid_policy():
    policy = SecurityPolicy(allow_filesystem=True)

    result = audit_security_policy(policy)

    assert result.passed is False
    assert result.failures


def test_security_audit_fails_for_network_access():
    policy = SecurityPolicy(allow_network=True)

    result = audit_security_policy(policy)

    assert result.passed is False
    assert "network access must be disabled" in result.failures
def test_security_audit_result_to_dict():
    result = SecurityAuditResult(
        passed=True,
        checks=["filesystem access disabled"],
        failures=[],
    )

    data = result.to_dict()

    assert data == {
        "passed": True,
        "checks": ["filesystem access disabled"],
        "failures": [],
    }
def test_security_audit_fails_for_multiple_restricted_capabilities():
    policy = SecurityPolicy(
        allow_filesystem=True,
        allow_network=True,
    )

    result = audit_security_policy(policy)

    assert result.passed is False
    assert "filesystem access must be disabled" in result.failures
    assert "network access must be disabled" in result.failures