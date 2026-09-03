import pytest

from src.wasm_loader import load_wasm
from wasmtime import Engine


def test_missing_wasm_file_is_rejected(tmp_path):
    missing_file = tmp_path / "missing.wasm"

    with pytest.raises(FileNotFoundError):
        load_wasm(str(missing_file), Engine())