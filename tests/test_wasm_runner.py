import pytest
from wasmtime import wat2wasm

from src.wasm_runner import run_wasm


def test_run_wasm_without_wasi(tmp_path):
    wat = """
    (module
      (func $_start nop)
      (export "_start" (func $_start))
    )
    """

    wasm_file = tmp_path / "test.wasm"
    wasm_file.write_bytes(wat2wasm(wat))

    run_wasm(str(wasm_file))


def test_run_wasm_rejects_invalid_fuel_limit(tmp_path):
    wat = """
    (module
      (func $_start nop)
      (export "_start" (func $_start))
    )
    """

    wasm_file = tmp_path / "invalid-fuel.wasm"
    wasm_file.write_bytes(wat2wasm(wat))

    with pytest.raises(
        ValueError,
        match="fuel_limit must be greater than zero",
    ):
        run_wasm(str(wasm_file), fuel_limit=0)
def test_run_wasm_rejects_invalid_memory_limit(tmp_path):
    wat = """
    (module
      (func $_start nop)
      (export "_start" (func $_start))
    )
    """

    wasm_file = tmp_path / "invalid-memory.wasm"
    wasm_file.write_bytes(wat2wasm(wat))

    with pytest.raises(
        ValueError,
        match="memory_limit must be greater than zero",
    ):
        run_wasm(str(wasm_file), memory_limit=0)
def test_run_wasm_rejects_missing_file(tmp_path):
    missing_file = tmp_path / "missing.wasm"

    with pytest.raises(FileNotFoundError):
        run_wasm(str(missing_file))