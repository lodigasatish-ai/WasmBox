from wasmtime import Engine, Linker, Module, Store, wat2wasm


def test_sandbox_does_not_provide_filesystem_host_imports():
    wat = """
    (module
      (import "filesystem" "read_file" (func $read_file))
    )
    """

    engine = Engine()
    store = Store(engine)
    module = Module(engine, wat2wasm(wat))

    linker = Linker(engine)

    try:
        linker.instantiate(store, module)
    except Exception:
        return

    raise AssertionError(
        "Filesystem host import should not be available by default"
    )