# BFT Dashboard

Web dashboard for running Board Functional Tests (BFT) on RF hardware.

## Stack

- **Backend**: FastAPI
- **Frontend**: NiceGUI
- **Package manager**: uv

---

## Folder Structure

```
bft_gui/
├── .python-version        # Locks Python version for uv
├── pyproject.toml         # Project dependencies
└── app/
    ├── __init__.py        # Marks app/ as a Python package
    ├── main.py            # FastAPI app, routes, and NiceGUI entry point
    ├── bft_tool.py        # Test definitions and subprocess execution
    ├── schemas.py         # Pydantic request/response models
    └── frontend.py        # NiceGUI dashboard UI
```

---

## Flow

### 1. Startup

```
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- FastAPI app starts and registers all API routes
- NiceGUI mounts onto the same FastAPI instance via `ui.run_with(app)`
- A single server serves both the API and the dashboard UI

### 2. User Opens the Dashboard

```
Browser → http://localhost:8000
```

- NiceGUI renders the dashboard
- Dashboard calls `GET /tests` to fetch available test names
- Test names are displayed as checkboxes (hidden by default)

### 3. User Configures and Starts a Run

```
User fills in Serial Number
User selects Run All or picks specific tests
User clicks Run
```

- Dashboard calls `POST /run` with `{ serial_no, tests }`
- FastAPI creates a global `current_run` with `status: "running"`
- Tests are dispatched to a background task immediately
- `POST /run` returns right away — dashboard does not block

### 4. Tests Execute in the Background

```
BackgroundTasks → BFTTool.run_selected()
```

- Each test runs one at a time via `subprocess.Popen`
- After each test completes, `on_result()` callback appends the result to `current_run.results`
- Dashboard polls `GET /run` every second and updates the results table live

### 5. Run Completes

```
current_run.status → "done" | "error" | "stopped"
```

- `"done"` — all selected tests finished
- `"error"` — an unexpected exception occurred
- `"stopped"` — user clicked Stop, current subprocess was terminated

### 6. User Stops a Run (Optional)

```
User clicks Stop
```

- Dashboard calls `POST /stop`
- FastAPI calls `BFTTool.stop()` which terminates the active subprocess
- `current_run.status` is set to `"stopped"`
- Results collected so far are preserved and displayed

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/health` | Liveness check |
| `GET`  | `/tests`  | List available test names |
| `POST` | `/run`    | Start a test run |
| `GET`  | `/run`    | Poll current run status and results |
| `POST` | `/stop`   | Stop the current run |

---

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://astral.sh/uv)

```bash
curl -Lf https://astral.sh/uv/install.sh | sh
```

### Install

```bash
cd harmony/bft_gui
uv sync
```

### Run

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access

| Interface | URL |
|-----------|-----|
| Dashboard | `http://localhost:8000` |
| API docs  | `http://localhost:8000/docs` |
| From another PC on the same network | `http://<host-ip>:8000` |