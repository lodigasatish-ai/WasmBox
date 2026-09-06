from src.resource_metrics import ResourceMetrics


def test_resource_metrics_to_dict():
    metrics = ResourceMetrics(
        execution_time_ms=1.5,
        memory_used_bytes=65536,
        peak_memory_bytes=131072,
        instruction_count=100,
        status="success",
    )

    result = metrics.to_dict()

    assert result == {
        "execution_time_ms": 1.5,
        "memory_used_bytes": 65536,
        "peak_memory_bytes": 131072,
        "instruction_count": 100,
        "status": "success",
    }