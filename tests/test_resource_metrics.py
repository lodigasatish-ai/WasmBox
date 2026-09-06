import tempfile
from pathlib import Path

from wasmtime import wat2wasm

from src.resource_metrics import ResourceMetrics
from src.wasm_runner import run_wasm


def test_resource_metrics_defaults():
    metrics = ResourceMetrics()

    assert metrics.execution_time_ms == 0.0
    assert metrics.memory_used_bytes == 0
    assert metrics.peak_memory_bytes == 0
    assert metrics.instruction_count == 0
    assert metrics.status == "unknown"


def test_execution_time_is_recorded():
    wat = """
    (module
      (func (export "_start")
        nop
      )
    )
    """

    wasm_bytes = wat2wasm(wat)

    with tempfile.TemporaryDirectory() as temp_dir:
        wasm_path = Path(temp_dir) / "test.wasm"
        wasm_path.write_bytes(wasm_bytes)

        metrics = run_wasm(
            str(wasm_path),
            return_metrics=True,
        )

    assert isinstance(metrics, ResourceMetrics)
    assert metrics.execution_time_ms >= 0
    assert metrics.status == "success"