import ast
import subprocess
import tempfile
from pathlib import Path


WIT_DIR = Path(__file__).resolve().parent / "wit"
WIT_WORLD = "hello"


def validate_python(code: str) -> None:
    """Validate Python syntax and reject obviously unsafe imports."""
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Python code cannot be empty.")

    try:
        ast.parse(code)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    blocked = {
        "os",
        "sys",
        "subprocess",
        "socket",
        "ctypes",
    }

    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name.split(".")[0] in blocked:
                    raise ValueError(f"Blocked import: {name.name}")

        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in blocked:
                raise ValueError(f"Blocked import: {node.module}")


def compile_python(code: str) -> bytes:
    """Compile Python source into a WASM component and return its bytes."""
    validate_python(code)

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

        result = subprocess.run(
            command,
            cwd=temp_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            error = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"Compilation failed: {error}")

        if not wasm_file.exists():
            raise RuntimeError("Compilation completed but WASM file was not created.")

        return wasm_file.read_bytes()