from pydantic import BaseModel
from typing import Literal

class RunRequest(BaseModel):
    serial_no: str
    tests: list[str]
class TestResult(BaseModel):
    name: str
    command: str
    status: Literal["pass", "fail", "running", "stopped"]
    duration: float | None = None
    output_path: str | None = None

class RunStatus(BaseModel):
    job_id: str
    serial_no: str
    status: Literal["running", "done", "error", "stopped"]
    results: list[TestResult] = []
    summary: str = ""