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
 
### Production mode
 
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Development mode

```bash
DEV_MODE=true uv run uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```
 
### Access
 
| Interface | URL |
|-----------|-----|
| Dashboard | `http://localhost:8000` |
| API docs  | `http://localhost:8000/api/docs` |
| From another PC on the same network | `http://<host-ip>:8000` |

### Demo

<img width="1631" height="860" alt="overview" src="https://github.com/user-attachments/assets/7759fa02-2be8-4dc1-ae7d-23c4e19cb14f" />


https://github.com/user-attachments/assets/6c07463e-1c03-4d3d-aa48-52cea537b09c
