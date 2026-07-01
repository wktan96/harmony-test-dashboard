from pydantic import BaseModel
from typing import Literal

# ─── Shared ───────────────────────────────────────────

class TestResult(BaseModel):
    name: str
    command: str
    status: Literal["pass", "fail", "running", "stopped"]
    duration: float | None = None
    output_path: str | None = None
    flow: str | None = None  # Only used for DVT results, indicates which flow the test belongs to

class RunStatus(BaseModel):
    job_id: int
    serial_no: str
    status: Literal["running", "done", "error", "stopped"]
    results: list[TestResult] = []
    summary: str = ""
    
# ─── BFT ──────────────────────────────────────────────

class BFTRunRequest(BaseModel):
    serial_no: str
    tests: list[str]

# ─── DVT ──────────────────────────────────────────────

class DVTRunRequest(BaseModel):
    serial_no: str
    temperature: Literal["25c", "60c", "-45c"]
    tests: list[str]