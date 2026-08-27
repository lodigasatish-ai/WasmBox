import time
import wasmtime

engine = wasmtime.Engine()
store = wasmtime.Store(engine)

component = wasmtime.Component.from_file(engine, "hello.wasm")
linker = wasmtime.Linker(engine)

instance = linker.instantiate(store, component)

hello = instance.get_func(store, "hello")

start = time.perf_counter()
result = hello(store)
end = time.perf_counter()

print("Result:", result)
print("Execution time:", (end - start) * 1000, "ms")