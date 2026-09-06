import tempfile
from pathlib import Path

from wasmtime import wat2wasm

from src.wasm_runner import run_wasm


def test_execution_time_is_measured():
    wat = """
    (module
      (func (export "_start")
        nop
        nop
        nop
        nop
      )
    )
    """

    wasm_bytes = wat2wasm(wat)

    with tempfile.TemporaryDirectory() as temp_dir:
        wasm_path = Path(temp_dir) / "execution_time.wasm"
        wasm_path.write_bytes(wasm_bytes)

        metrics = run_wasm(
            str(wasm_path),
            return_metrics=True,
        )

    assert metrics.execution_time_ms >= 0
    assert metrics.status == "success"