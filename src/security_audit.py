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