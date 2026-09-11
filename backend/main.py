from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="WasmBox Backend API",
    description="Backend API for the WasmBox secure multi-tenant plugin sandbox",
    version="1.0.0"
)


class RunRequest(BaseModel):
    code: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/run")
def run_code(request: RunRequest):
    return {
        "success": True,
        "output": request.code
    }