from dataclasses import dataclass


@dataclass
class ResourceMetrics:
    """Resource usage metrics collected during WASM execution."""

    execution_time_ms: float = 0.0
    memory_used_bytes: int = 0
    peak_memory_bytes: int = 0
    instruction_count: int = 0
    status: str = "unknown"