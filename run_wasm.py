import time
import wasmtime
from hello_host import Root

engine = wasmtime.Engine()
store = wasmtime.Store(engine)

root = Root(store)

start = time.perf_counter()
result = root.hello(store)
end = time.perf_counter()

print("Result:", result)
print("Execution time:", (end - start) * 1000, "ms")