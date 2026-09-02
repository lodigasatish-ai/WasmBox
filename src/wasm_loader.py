from pathlib import Path

from wasmtime import Engine, Module


def load_wasm(wasm_path: str, engine: Engine) -> Module:
    """Safely load and compile a WASM module from disk."""
    path = Path(wasm_path)

    if not path.is_file():
        raise FileNotFoundError(f"WASM module not found: {path}")

    if path.suffix.lower() != ".wasm":
        raise ValueError("Only .wasm files are supported")

    return Module.from_file(engine, str(path))