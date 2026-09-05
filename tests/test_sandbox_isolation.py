import pytest
from wasmtime import Engine, Linker, Module, Store, wat2wasm
from src.sandbox_runtime import SandboxRuntime

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
        from src.sandbox_runtime import SandboxRuntime


def test_sandbox_memory_limit_is_10_mb():
    runtime = SandboxRuntime()

    store = runtime.create_store()

    assert runtime.memory_limit == 10 * 1024 * 1024