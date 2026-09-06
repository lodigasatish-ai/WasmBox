import tempfile
from pathlib import Path

from wasmtime import wat2wasm

from src.resource_metrics import ResourceMetrics
from src.wasm_runner import run_wasm


def test_limit_exceeded_status_is_reported():
    wat = """
    (module
      (func (export "_start")
        (loop
          br 0
        )
      )
    )
    """

    wasm_bytes = wat2wasm(wat)

    with tempfile.TemporaryDirectory() as temp_dir:
        wasm_path = Path(temp_dir) / "limit_metrics.wasm"
        wasm_path.write_bytes(wasm_bytes)

        metrics = run_wasm(
            str(wasm_path),
            fuel_limit=100,
            return_metrics=True,
        )

    assert isinstance(metrics, ResourceMetrics)
    assert metrics.status == "limit_exceeded"
    assert metrics.execution_time_ms >= 0
    assert metrics.instruction_count > 0