from dataclasses import asdict, dataclass


@dataclass
class SecurityAuditResult:
    """Result of a sandbox security audit."""

    passed: bool
    checks: list[str]
    failures: list[str]

    def to_dict(self) -> dict:
        """Convert the audit result into a backend-friendly dictionary."""
        return asdict(self)
    from src.security_policy import SecurityPolicy


def audit_security_policy(policy: SecurityPolicy) -> SecurityAuditResult:
    """Audit the sandbox security policy."""

    checks = []
    failures = []

    try:
        policy.validate()
        checks.append("security policy validation")
    except ValueError as exc:
        failures.append(str(exc))

    return SecurityAuditResult(
        passed=not failures,
        checks=checks,
        failures=failures,
    )