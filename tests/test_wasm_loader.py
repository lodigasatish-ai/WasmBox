import pytest
from wasmtime import Engine, wat2wasm

from src.wasm_loader import load_wasm


def test_load_wasm_module(tmp_path):
    wat = """
    (module
      (func $_start nop)
      (export "_start" (func $_start))
    )
    """

    wasm_file = tmp_path / "valid.wasm"
    wasm_file.write_bytes(wat2wasm(wat))

    engine = Engine()
    module = load_wasm(str(wasm_file), engine)

    assert module is not None


def test_load_wasm_requires_wasm_extension(tmp_path):
    invalid_file = tmp_path / "plugin.txt"
    invalid_file.write_bytes(b"not wasm")

    with pytest.raises(ValueError, match="Only .wasm files are supported"):
        load_wasm(str(invalid_file), Engine())


def test_load_wasm_rejects_missing_file(tmp_path):
    missing_file = tmp_path / "missing.wasm"

    with pytest.raises(FileNotFoundError):
        load_wasm(str(missing_file), Engine())