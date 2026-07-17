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

[Screencast from 07-17-2026 04:14:02 PM.webm](https://github.com/user-attachments/assets/48dde56a-44ff-4b14-9be4-daf17e1ec1a9)
