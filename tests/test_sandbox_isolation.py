import pytest
from wasmtime import Engine, Linker, Module, Store, wat2wasm


def test_module_with_unavailable_host_import_is_rejected():
    wat = """
    (module
      (import "host" "secret" (func $secret))
      (func $_start
        call $secret
      )
      (export "_start" (func $_start))
    )
    """

    engine = Engine()
    store = Store(engine)
    module = Module(engine, wat2wasm(wat))

    linker = Linker(engine)

    with pytest.raises(Exception):
        linker.instantiate(store, module)