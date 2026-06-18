import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Creates tables if they don't exist. Called once on startup."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    job_id      TEXT PRIMARY KEY,
                    type        TEXT NOT NULL,
                    serial_no   TEXT NOT NULL,
                    status      TEXT NOT NULL,
                    summary     TEXT,
                    temperature TEXT,
                    created_at  TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    id          SERIAL PRIMARY KEY,
                    job_id      TEXT REFERENCES runs(job_id),
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
            cur.execute("""
                INSERT INTO runs (job_id, type, serial_no, status, summary, temperature)
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
            cur.execute("DELETE FROM test_results WHERE job_id = %s", (job_id,))
            for r in results:
                cur.execute("""
                    INSERT INTO test_results (job_id, name, command, status, duration, output_path, flow)
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
            cur.execute("SELECT * FROM runs ORDER BY created_at DESC")
            return cur.fetchall()


def get_run_by_id(job_id: str) -> dict | None:
    """Returns a single run with all its test results."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM runs WHERE job_id = %s", (job_id,))
            run = cur.fetchone()
            if not run:
                return None
            cur.execute("SELECT * FROM test_results WHERE job_id = %s ORDER BY id", (job_id,))
            run["results"] = cur.fetchall()
            return run