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