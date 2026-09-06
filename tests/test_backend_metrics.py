import tempfile
from pathlib import Path

from wasmtime import wat2wasm

from src.wasm_runner import run_wasm


def test_run_wasm_returns_backend_metrics():
    wat = """
    (module
      (memory (export "memory") 1 2)
      (func (export "_start")
        nop
        nop
      )
    )
    """

    wasm_bytes = wat2wasm(wat)

    with tempfile.TemporaryDirectory() as temp_dir:
        wasm_path = Path(temp_dir) / "backend_metrics.wasm"
        wasm_path.write_bytes(wasm_bytes)

        metrics = run_wasm(
            str(wasm_path),
            return_metrics=True,
        )

    result = metrics.to_dict()

    assert "execution_time_ms" in result
    assert "memory_used_bytes" in result
    assert "peak_memory_bytes" in result
    assert "instruction_count" in result
    assert "status" in result

    assert result["execution_time_ms"] >= 0
    assert result["memory_used_bytes"] == 64 * 1024
    assert result["peak_memory_bytes"] == 64 * 1024
    assert result["instruction_count"] > 0
    assert result["status"] == "success"