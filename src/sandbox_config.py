from wasmtime import Config


def create_sandbox_config() -> Config:
    """Create a Wasmtime configuration for isolated plugin execution."""
    config = Config()

    # Enable fuel consumption so execution can be bounded.
    config.consume_fuel = True

    return config