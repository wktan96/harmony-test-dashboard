from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from nicegui import ui
from app.schemas import RunRequest, RunStatus, TestResult
from app.bft_tool import BFTTool, AVAILABLE_TESTS
from app import frontend  # noqa: F401

app = FastAPI(title="BFT Dashboard API", version="0.4.0")

jobs: dict[str, RunStatus] = {}             # stores all runs by job_id
current_tool: BFTTool | None = None         # reference for stop()
current_job_id: str | None = None


def run_bft_job(job_id: str, serial_no: str, selected_tests: list[str]):
    global current_tool

    def on_result(result: dict):
        existing = next((r for r in jobs[job_id].results if r.name == result["name"]), None)
        if existing:
            existing.status = result["status"]
            existing.duration = result.get("duration")
        else:
            # **result unpacks the dict into keyword arguments for TestResult, 
            # which is equivalent to TestResult(name="cal_set_freq_test", command="sleep 10", status="running", duration=None)
            jobs[job_id].results.append(TestResult(**result))

    try:
        current_tool.run_selected(selected_tests, on_result)

        if jobs[job_id].status != "stopped":
            passed = sum(1 for r in jobs[job_id].results if r.status == "pass")
            jobs[job_id].summary = f"{passed}/{len(selected_tests)} passed"
            jobs[job_id].status = "done"
        else:
            running = next((r for r in jobs[job_id].results if r.status == "running"), None)
            if running:
                running.status = "stopped"

    except Exception as e:
        jobs[job_id].status = "error"
        jobs[job_id].summary = str(e)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tests", response_model=list[str])
def list_available_tests():
    return AVAILABLE_TESTS


@app.post("/run", response_model=RunStatus, status_code=202)
def start_run(request: RunRequest, background_tasks: BackgroundTasks):
    global current_job_id, current_tool

    if not request.serial_no.strip():
        raise HTTPException(status_code=422, detail="serial_no cannot be empty")

    if current_job_id and jobs[current_job_id].status == "running":
        raise HTTPException(status_code=409, detail="A run is already in progress")

    job_id = datetime.now().strftime("%Y%m%d_%H%M%S")  # e.g. "20260513_143022"
    current_job_id = job_id
    current_tool = BFTTool(serial_no=request.serial_no)

    jobs[job_id] = RunStatus(
        job_id=job_id,
        serial_no=request.serial_no,
        status="running"
    )

    background_tasks.add_task(run_bft_job, job_id, request.serial_no, request.tests)

    return jobs[job_id]

@app.get("/run/current", response_model=RunStatus)
def get_current_run():
    """Returns the latest run — used by the frontend to poll."""
    if current_job_id is None:
        raise HTTPException(status_code=404, detail="No run has been started yet")
    return jobs[current_job_id]


@app.get("/run/{job_id}", response_model=RunStatus)
def get_run_by_id(job_id: str):
    """Returns a specific run by job_id — used for history review."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]


@app.get("/runs", response_model=list[RunStatus])
def list_runs():
    """Returns all runs — used to populate the history list."""
    return list(jobs.values())


@app.post("/stop", response_model=RunStatus)
def stop_run():
    global current_tool

    if current_job_id is None or jobs[current_job_id].status != "running":
        raise HTTPException(status_code=400, detail="No active run to stop")

    current_tool.stop()
    jobs[current_job_id].status = "stopped"

    passed = sum(1 for r in jobs[current_job_id].results if r.status == "pass")
    total = len(jobs[current_job_id].results)
    jobs[current_job_id].summary = f"{passed}/{total} passed (stopped)"

    return jobs[current_job_id]


ui.run_with(app, title="BFT Dashboard")