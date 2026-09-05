from src.resource_metrics import ResourceMetrics


def test_resource_metrics_defaults():
    metrics = ResourceMetrics()

    assert metrics.execution_time_ms == 0.0
    assert metrics.memory_used_bytes == 0
    assert metrics.peak_memory_bytes == 0
    assert metrics.instruction_count == 0
    assert metrics.status == "unknown"