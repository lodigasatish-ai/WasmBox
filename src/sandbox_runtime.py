from wasmtime import Config, Engine, Store


DEFAULT_MEMORY_LIMIT = 10 * 1024 * 1024


class SandboxRuntime:
    """Creates a restricted Wasmtime runtime for plugin execution."""

    def __init__(
        self,
        fuel_limit: int = 100_000,
        memory_limit: int = DEFAULT_MEMORY_LIMIT,
    ):
        if fuel_limit <= 0:
            raise ValueError("fuel_limit must be greater than zero")

        if memory_limit <= 0:
            raise ValueError("memory_limit must be greater than zero")

        config = Config()
        config.consume_fuel = True

        self.engine = Engine(config)
        self.fuel_limit = fuel_limit
        self.memory_limit = memory_limit

    def create_store(self) -> Store:
        """Create a fresh store with configured resource limits."""
        store = Store(self.engine)
        store.set_fuel(self.fuel_limit)
        store.set_limits(memory_size=self.memory_limit)
        return store