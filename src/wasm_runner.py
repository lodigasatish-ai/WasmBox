from pathlib import Path

from wasmtime import Engine, Linker, Module, Store


def run_wasm(wasm_path: str) -> int:
    """Load and execute a Wasm module with no host imports."""
    path = Path(wasm_path)

    if not path.is_file():
        raise FileNotFoundError(f"Wasm module not found: {path}")

    engine = Engine()
    store = Store(engine)
    module = Module.from_file(engine, str(path))

    linker = Linker(engine)
    instance = linker.instantiate(store, module)

    start = instance.exports(store).get("_start")

    if start is not None:
        start(store)

    return 0