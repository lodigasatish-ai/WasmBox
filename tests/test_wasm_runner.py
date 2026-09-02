from wasmtime import wat2wasm

from src.wasm_runner import run_wasm


def test_run_simple_wasm(tmp_path):
    wat = """
    (module
      (func $_start
        nop
      )
      (export "_start" (func $_start))
    )
    """

    wasm_file = tmp_path / "hello.wasm"
    wasm_file.write_bytes(wat2wasm(wat))

    assert run_wasm(str(wasm_file)) == 0