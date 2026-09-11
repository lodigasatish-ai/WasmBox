import ast
import hashlib
import subprocess
import tempfile
import time
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
WIT_DIR = PROJECT_DIR / "wit"
CACHE_DIR = PROJECT_DIR / ".wasm_cache"
WIT_WORLD = "hello"


def validate_python(code: str) -> None:
    """Validate Python syntax and reject obviously unsafe imports."""
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Python code cannot be empty.")

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    blocked = {
        "os",
        "sys",
        "subprocess",
        "socket",
        "ctypes",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name.split(".")[0] in blocked:
                    raise ValueError(f"Blocked import: {name.name}")

        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in blocked:
                raise ValueError(f"Blocked import: {node.module}")


def get_cache_key(code: str) -> str:
    """Create a unique cache key for the Python code and WIT files."""
    hasher = hashlib.sha256()

    hasher.update(code.encode("utf-8"))

    for wit_file in sorted(WIT_DIR.rglob("*")):
        if wit_file.is_file():
            hasher.update(wit_file.relative_to(WIT_DIR).as_posix().encode("utf-8"))
            hasher.update(wit_file.read_bytes())

    return hasher.hexdigest()


def compile_python(code: str) -> bytes:
    """Compile Python source into a WASM component and use a local cache."""
    validate_python(code)

    CACHE_DIR.mkdir(exist_ok=True)

    cache_key = get_cache_key(code)
    cache_file = CACHE_DIR / f"{cache_key}.wasm"

    if cache_file.exists():
        print("Cache hit: returning existing WASM.")
        return cache_file.read_bytes()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        source_file = temp_path / "hello.py"
        wasm_file = temp_path / "output.wasm"

        source_file.write_text(code, encoding="utf-8")

        command = [
            "componentize-py",
            "-d",
            str(WIT_DIR),
            "-w",
            WIT_WORLD,
            "componentize",
            "--stub-wasi",
            "hello",
            "-o",
            str(wasm_file),
        ]

        start_time = time.perf_counter()

        result = subprocess.run(
            command,
            cwd=temp_path,
            capture_output=True,
            text=True,
        )

        compile_time = time.perf_counter() - start_time
        print(f"Compilation time: {compile_time * 1000:.2f} ms")

        if result.returncode != 0:
            error = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"Compilation failed: {error}")

        if not wasm_file.exists():
            raise RuntimeError(
                "Compilation completed but WASM file was not created."
            )

        wasm_data = wasm_file.read_bytes()

        cache_file.write_bytes(wasm_data)

        print("WASM saved to cache.")

        return wasm_data