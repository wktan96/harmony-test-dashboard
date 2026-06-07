# Web Dashboard
 
Web dashboard for running functional and performance tests on RF hardware.
 
## Stack
 
- **Backend**: FastAPI
- **Frontend**: NiceGUI
- **Package manager**: uv
---
 
## Setup
 
### Prerequisites
 
- Python 3.11+
- [uv](https://astral.sh/uv)
```bash
curl -Lf https://astral.sh/uv/install.sh | sh
```
 
### Install Dependency
 
```bash
uv sync
```
 
### Run
 
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```
 
### Access
 
| Interface | URL |
|-----------|-----|
| Dashboard | `http://localhost:8000` |
| API docs  | `http://localhost:8000/api/docs` |
| From another PC on the same network | `http://<host-ip>:8000` |