from dataclasses import dataclass, field

from src.security_policy import SecurityPolicy
from src.sandbox_runtime import SandboxRuntime


@dataclass
class SecurityAuditResult:
    """Result of a sandbox security policy audit."""

    passed: bool
    checks: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert the audit result into a backend-friendly dictionary."""
        return {
            "passed": self.passed,
            "checks": self.checks,
            "failures": self.failures,
        }

def audit_security_policy(policy: SecurityPolicy) -> SecurityAuditResult:
    """Audit the sandbox policy for required security restrictions."""

    checks = []
    failures = []

    # Check that the security policy itself is valid.
    try:
        policy.validate()
        checks.append("security policy validation")
    except ValueError as exc:
        failures.append(str(exc))

    # Check filesystem access is disabled.
    if policy.allow_filesystem:
        failures.append("filesystem access must be disabled")
    else:
        checks.append("filesystem access disabled")

    # Check network access is disabled.
    if policy.allow_network:
        failures.append("network access must be disabled")
    else:
        checks.append("network access disabled")

    return SecurityAuditResult(
        passed=not failures,
        checks=checks,
        failures=failures,
    )


def audit_sandbox_runtime(runtime: SandboxRuntime) -> SecurityAuditResult:
    """Audit the sandbox runtime for required resource limits."""

    checks = []
    failures = []

    if runtime.fuel_limit > 0:
        checks.append("fuel limit configured")
    else:
        failures.append("fuel limit must be greater than zero")

    if runtime.memory_limit > 0:
        checks.append("memory limit configured")
    else:
        failures.append("memory limit must be greater than zero")

    return SecurityAuditResult(
        passed=not failures,
        checks=checks,
        failures=failures,
    )

def audit_wasm_imports(module) -> SecurityAuditResult:
    """Audit a WASM module to ensure it does not import unsafe host capabilities."""

    checks = []
    failures = []

    for import_item in module.imports:
        module_name = import_item.module

        if module_name in {"wasi_snapshot_preview1", "wasi_unstable"}:
            failures.append(
                f"unsafe WASI import detected: {module_name}"
            )
        else:
            checks.append(
                f"allowed import: {module_name}"
            )

    return SecurityAuditResult(
        passed=not failures,
        checks=checks,
        failures=failures,
    )