from src.security_audit import SecurityAuditResult, audit_security_policy
from src.security_policy import SecurityPolicy


def test_security_audit_passes_for_valid_policy():
    policy = SecurityPolicy()

    result = audit_security_policy(policy)

    assert isinstance(result, SecurityAuditResult)
    assert result.passed is True
    assert "security policy validation" in result.checks
    assert result.failures == []