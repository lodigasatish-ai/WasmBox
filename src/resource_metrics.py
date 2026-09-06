from dataclasses import dataclass


WASM_PAGE_SIZE = 64 * 1024


@dataclass
class ResourceMetrics:
    """Resource usage metrics collected during WASM execution."""

    execution_time_ms: float = 0.0
    memory_used_bytes: int = 0
    peak_memory_bytes: int = 0
    instruction_count: int = 0
    status: str = "unknown"


def memory_size_bytes(memory, store) -> int:
    """Return the current WASM linear memory size in bytes."""
    return memory.size(store) * WASM_PAGE_SIZE