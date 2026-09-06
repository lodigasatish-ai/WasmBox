import tempfile
from pathlib import Path

from wasmtime import wat2wasm

from src.resource_metrics import WASM_PAGE_SIZE
from src.wasm_runner import run_wasm


def test_memory_usage_is_recorded():
    wat = """
    (module
      (memory (export "memory") 1 2)
      (func (export "_start")
        i32.const 1
        memory.grow
        drop
      )
    )
    """

    wasm_bytes = wat2wasm(wat)

    with tempfile.TemporaryDirectory() as temp_dir:
        wasm_path = Path(temp_dir) / "memory_test.wasm"
        wasm_path.write_bytes(wasm_bytes)

        metrics = run_wasm(
            str(wasm_path),
            return_metrics=True,
        )

    assert metrics.memory_used_bytes == 2 * WASM_PAGE_SIZE
    assert metrics.peak_memory_bytes == 2 * WASM_PAGE_SIZE
    assert metrics.status == "success"