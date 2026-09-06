import tempfile
from pathlib import Path

import pytest
from wasmtime import Trap, wat2wasm

from src.wasm_runner import run_wasm


def test_execution_time_limit_stops_long_execution():
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
        wasm_path = Path(temp_dir) / "time_limit_test.wasm"
        wasm_path.write_bytes(wasm_bytes)

        with pytest.raises(Trap):
            run_wasm(
                str(wasm_path),
                fuel_limit=100,
            )