from pathlib import Path
import time

from wasmtime import Engine, Linker, Module, Store

from src.security_policy import SecurityPolicy
from src.resource_metrics import ResourceMetrics


def run_wasm(
    wasm_path: str,
    policy: SecurityPolicy | None = None,
    fuel_limit: int = 100_000,
    return_metrics: bool = False,
) -> int | ResourceMetrics:
    """Execute a WASM module without granting filesystem or network imports."""

    path = Path(wasm_path)

    if not path.is_file():
        raise FileNotFoundError(f"Wasm module not found: {path}")

    if path.suffix.lower() != ".wasm":
        raise ValueError("Only .wasm files are supported")

    if fuel_limit <= 0:
        raise ValueError("fuel_limit must be greater than zero")

    policy = policy or SecurityPolicy()
    policy.validate()

    engine_config = __import__("wasmtime").Config()
    engine_config.consume_fuel = True

    engine = Engine(engine_config)
    store = Store(engine)
    store.set_fuel(fuel_limit)

    module = Module.from_file(engine, str(path))

    # Deliberately do not provide filesystem or network host imports.
    linker = Linker(engine)
    instance = linker.instantiate(store, module)

    metrics = ResourceMetrics()
    start_time = time.perf_counter()

    start = instance.exports(store).get("_start")

    if start is not None:
        start(store)

    end_time = time.perf_counter()

    metrics.execution_time_ms = (end_time - start_time) * 1000
    metrics.status = "success"

    if return_metrics:
        return metrics

    return 0