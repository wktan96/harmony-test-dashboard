import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from app.config import DEV_MODE

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Dynamic table configuration based on configuration state
RUNS_TABLE = "dev_runs" if DEV_MODE else "runs"
RESULTS_TABLE = "dev_test_results" if DEV_MODE else "test_results"


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Creates tables if they don't exist. Called once on startup."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Initialize appropriate tables depending on DEV_MODE status
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {RUNS_TABLE} (
                    job_id      TEXT PRIMARY KEY,
                    type        TEXT NOT NULL,
                    serial_no   TEXT NOT NULL,
                    status      TEXT NOT NULL,
                    summary     TEXT,
                    temperature TEXT,
                    created_at  TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {RESULTS_TABLE} (
                    id          SERIAL PRIMARY KEY,
                    job_id      TEXT REFERENCES {RUNS_TABLE}(job_id) ON DELETE CASCADE,
                    name        TEXT NOT NULL,
                    command     TEXT,
                    status      TEXT NOT NULL,
                    duration    REAL,
                    output_path TEXT,
                    flow        TEXT
                );
            """)
        conn.commit()


def save_run(job_id: str, run_type: str, serial_no: str, status: str, summary: str, temperature: str = None):
    """Saves or updates a run record."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {RUNS_TABLE} (job_id, type, serial_no, status, summary, temperature)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (job_id) DO UPDATE
                SET status = EXCLUDED.status,
                    summary = EXCLUDED.summary;
            """, (job_id, run_type, serial_no, status, summary, temperature))
        conn.commit()


def save_test_results(job_id: str, results: list):
    """Saves all test results for a run."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {RESULTS_TABLE} WHERE job_id = %s", (job_id,))
            for r in results:
                cur.execute(f"""
                    INSERT INTO {RESULTS_TABLE} (job_id, name, command, status, duration, output_path, flow)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    job_id,
                    r.name,
                    r.command,
                    r.status,
                    r.duration,
                    r.output_path,
                    getattr(r, "flow", None)
                ))
        conn.commit()


def get_all_runs() -> list:
    """Returns all runs ordered by most recent first."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SELECT * FROM {RUNS_TABLE} ORDER BY created_at DESC")
            return cur.fetchall()


def get_run_by_id(job_id: str) -> dict | None:
    """Returns a single run with all its test results."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SELECT * FROM {RUNS_TABLE} WHERE job_id = %s", (job_id,))
            run = cur.fetchone()
            if not run:
                return None
            cur.execute(f"SELECT * FROM {RESULTS_TABLE} WHERE job_id = %s ORDER BY id", (job_id,))
            run["results"] = cur.fetchall()
            return run