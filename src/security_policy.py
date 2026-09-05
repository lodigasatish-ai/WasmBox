from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityPolicy:
    """Capabilities available to an untrusted WASM module."""

    allow_filesystem: bool = False
    allow_network: bool = False

    def validate(self) -> None:
        """Reject policies that accidentally enable restricted capabilities."""
        if self.allow_filesystem:
            raise ValueError("Filesystem access is disabled by default")

        if self.allow_network:
            raise ValueError("Network access is disabled by default")