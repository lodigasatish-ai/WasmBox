from wasmtime import Config, Engine, Store


class SandboxRuntime:
    """Creates a restricted Wasmtime runtime for plugin execution."""

    def __init__(self, fuel_limit: int = 100_000):
        if fuel_limit <= 0:
            raise ValueError("fuel_limit must be greater than zero")

        config = Config()
        config.consume_fuel = True

        self.engine = Engine(config)
        self.fuel_limit = fuel_limit

    def create_store(self) -> Store:
        """Create a fresh store with the configured execution budget."""
        store = Store(self.engine)
        store.set_fuel(self.fuel_limit)
        return store