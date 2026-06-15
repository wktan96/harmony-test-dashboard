from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from nicegui import ui
from app.schemas import BFTRunRequest, DVTRunRequest, RunStatus, TestResult
from app.bft_tool import BFTTool, BFT_TESTS
from app.dvt_tool import DVTTool, DVT_TESTS, DVT_FLOWS, PRESET_3GHZ_REDUCED_TESTS, PRESET_6GHZ_REDUCED_TESTS
from app import frontend  # noqa: F401

app = FastAPI(title="BFT Dashboard API", version="0.5.0")

# ─── BFT globals ──────────────────────────────────────
jobs: dict[str, RunStatus] = {}
current_job_id: str | None = None
current_tool: BFTTool | None = None

# ─── DVT globals ──────────────────────────────────────
dvt_jobs: dict[str, RunStatus] = {}
dvt_current_job_id: str | None = None
dvt_current_tool: DVTTool | None = None

# ─── BFT background job ───────────────────────────────
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

# ─── DVT background job ───────────────────────────────
def run_dvt_job(job_id: str, serial_no: str, selected_tests: list[str]):
    global dvt_current_tool

    def on_result(result: dict):
        result["flow"] = dvt_current_tool.get_test_flow(result["name"])
        existing = next((r for r in dvt_jobs[job_id].results if r.name == result["name"]), None)
        if existing:
            existing.status = result["status"]
            existing.duration = result.get("duration")
        else:
            dvt_jobs[job_id].results.append(TestResult(**result))

    try:
        dvt_current_tool.run_selected(selected_tests, on_result)

        if dvt_jobs[job_id].status != "stopped":
            passed = sum(1 for r in dvt_jobs[job_id].results if r.status == "pass")
            dvt_jobs[job_id].summary = f"{passed}/{len(selected_tests)} passed"
            dvt_jobs[job_id].status = "done"
        else:
            running = next((r for r in dvt_jobs[job_id].results if r.status == "running"), None)
            if running:
                running.status = "stopped"

    except Exception as e:
        dvt_jobs[job_id].status = "error"
        dvt_jobs[job_id].summary = str(e)

# ─── BFT endpoints ────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/bft/tests", response_model=list[str])
def list_available_tests():
    return BFT_TESTS

@app.post("/run", response_model=RunStatus, status_code=202)
def start_run(request: BFTRunRequest, background_tasks: BackgroundTasks):
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

# ─── DVT endpoints ────────────────────────────────────
@app.get("/dvt/tests", response_model=list[str])
def list_dvt_tests():
    return DVT_TESTS

@app.get("/dvt/flows")
def list_dvt_flows():
    return DVT_FLOWS

@app.get("/dvt/presets/3ghz-reduced", response_model=list[str])
def get_3ghz_reduced_preset():
    return PRESET_3GHZ_REDUCED_TESTS

@app.get("/dvt/presets/6ghz-reduced", response_model=list[str])
def get_6ghz_reduced_preset():
    return PRESET_6GHZ_REDUCED_TESTS

@app.post("/dvt/run", response_model=RunStatus, status_code=202)
def start_dvt_run(request: DVTRunRequest, background_tasks: BackgroundTasks):
    global dvt_current_job_id, dvt_current_tool

    if not request.serial_no.strip():
        raise HTTPException(status_code=422, detail="serial_no cannot be empty")

    if dvt_current_job_id and dvt_jobs[dvt_current_job_id].status == "running":
        raise HTTPException(status_code=409, detail="A DVT run is already in progress")

    job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    dvt_current_job_id = job_id
    dvt_current_tool = DVTTool(
        serial_no=request.serial_no,
        temperature=request.temperature
    )

    dvt_jobs[job_id] = RunStatus(
        job_id=job_id,
        serial_no=request.serial_no,
        status="running"
    )

    background_tasks.add_task(run_dvt_job, job_id, request.serial_no, request.tests)

    return dvt_jobs[job_id]


@app.get("/dvt/run/current", response_model=RunStatus)
def get_current_dvt_run():
    if dvt_current_job_id is None:
        raise HTTPException(status_code=404, detail="No DVT run has been started yet")
    return dvt_jobs[dvt_current_job_id]


@app.post("/dvt/stop", response_model=RunStatus)
def stop_dvt_run():
    global dvt_current_tool

    if dvt_current_job_id is None or dvt_jobs[dvt_current_job_id].status != "running":
        raise HTTPException(status_code=400, detail="No active DVT run to stop")

    dvt_current_tool.stop()
    dvt_jobs[dvt_current_job_id].status = "stopped"

    passed = sum(1 for r in dvt_jobs[dvt_current_job_id].results if r.status == "pass")
    total = len(dvt_jobs[dvt_current_job_id].results)
    dvt_jobs[dvt_current_job_id].summary = f"{passed}/{total} passed (stopped)"

    return dvt_jobs[dvt_current_job_id]


# ─── Mount NiceGUI ────────────────────────────────────
ui.run_with(app, title="Harmony Test Dashboard")