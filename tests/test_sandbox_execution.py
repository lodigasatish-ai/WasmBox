from wasmtime import Engine, Linker, Module, Store, wat2wasm


def test_sandbox_can_execute_wasm_without_host_imports():
    wat = """
    (module
      (func $_start
        nop
      )
      (export "_start" (func $_start))
    )
    """

    engine = Engine()
    store = Store(engine)
    module = Module(engine, wat2wasm(wat))

    linker = Linker(engine)
    instance = linker.instantiate(store, module)

    start = instance.exports(store)["_start"]
    start(store)
    