import tempfile
from pathlib import Path

from wasmtime import wat2wasm

from src.resource_metrics import ResourceMetrics
from src.wasm_runner import run_wasm


def test_instruction_count_is_recorded():
    wat = """
    (module
      (func (export "_start")
        nop
        nop
        nop
      )
    )
    """

    wasm_bytes = wat2wasm(wat)

    with tempfile.TemporaryDirectory() as temp_dir:
        wasm_path = Path(temp_dir) / "instruction_test.wasm"
        wasm_path.write_bytes(wasm_bytes)

        metrics = run_wasm(
            str(wasm_path),
            return_metrics=True,
        )

    assert isinstance(metrics, ResourceMetrics)
    assert metrics.instruction_count > 0
    assert metrics.status == "success"