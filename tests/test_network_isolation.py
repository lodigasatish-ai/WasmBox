import pytest
from wasmtime import Engine, Linker, Module, Store, wat2wasm


def test_sandbox_does_not_provide_network_host_imports():
    wat = """
    (module
      (import "network" "connect" (func $connect))
    )
    """

    engine = Engine()
    store = Store(engine)
    module = Module(engine, wat2wasm(wat))

    linker = Linker(engine)

    with pytest.raises(Exception):
        linker.instantiate(store, module)