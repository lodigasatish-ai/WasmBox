import ast
import hashlib
import logging
import subprocess
import tempfile
import time
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
WIT_DIR = PROJECT_DIR / "wit"
CACHE_DIR = PROJECT_DIR / ".wasm_cache"
LOG_FILE = PROJECT_DIR / "compiler.log"
WIT_WORLD = "hello"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def validate_python(code: str) -> None:
    """Validate Python syntax and reject obviously unsafe imports."""
    if not isinstance(code, str) or not code.strip():
        logging.warning("Validation failed: empty Python code.")
        raise ValueError("Python code cannot be empty.")

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        logging.warning("Validation failed: invalid Python syntax.")
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
                    logging.warning(f"Blocked import: {name.name}")
                    raise ValueError(f"Blocked import: {name.name}")

        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in blocked:
                logging.warning(f"Blocked import: {node.module}")
                raise ValueError(f"Blocked import: {node.module}")


def get_cache_key(code: str) -> str:
    """Create a unique cache key for the Python code and WIT files."""
    hasher = hashlib.sha256()

    hasher.update(code.encode("utf-8"))

    for wit_file in sorted(WIT_DIR.rglob("*")):
        if wit_file.is_file():
            hasher.update(
                wit_file.relative_to(WIT_DIR).as_posix().encode("utf-8")
            )
            hasher.update(wit_file.read_bytes())

    return hasher.hexdigest()


def compile_python(code: str) -> bytes:
    """Compile Python source into a WASM component and use a local cache."""
    logging.info("Compilation request received.")

    validate_python(code)

    CACHE_DIR.mkdir(exist_ok=True)

    cache_key = get_cache_key(code)
    cache_file = CACHE_DIR / f"{cache_key}.wasm"

    if cache_file.exists():
        logging.info("Cache hit.")
        print("Cache hit: returning existing WASM.")
        return cache_file.read_bytes()

    logging.info("Cache miss. Starting WASM compilation.")

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

            logging.error(f"Compilation failed: {error}")

            raise RuntimeError(f"Compilation failed: {error}")

        if not wasm_file.exists():
            logging.error("Compilation completed but WASM file was not created.")

            raise RuntimeError(
                "Compilation completed but WASM file was not created."
            )

        wasm_data = wasm_file.read_bytes()

        cache_file.write_bytes(wasm_data)

        logging.info(
            f"Compilation successful. Time: "
            f"{compile_time * 1000:.2f} ms, "
            f"WASM size: {len(wasm_data)} bytes."
        )

        print("WASM saved to cache.")

        return wasm_data