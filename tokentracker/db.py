"""SQLite storage for API call logs. Zero config, works out of the box."""

from __future__ import annotations

import os
import sqlite3
import time
from pathlib import Path
from threading import local

_thread_local = local()

DEFAULT_DB_PATH = os.environ.get(
    "TOKENTRACKER_DB",
    str(Path.home() / ".tokentracker" / "usage.db"),
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    model TEXT NOT NULL,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    cost_usd REAL,
    latency_ms REAL,
    endpoint TEXT,
    status TEXT DEFAULT 'ok',
    error TEXT,
    metadata TEXT
);
CREATE INDEX IF NOT EXISTS idx_calls_timestamp ON calls(timestamp);
CREATE INDEX IF NOT EXISTS idx_calls_model ON calls(model);
"""


def get_db(db_path: str | None = None) -> sqlite3.Connection:
    """Get a thread-local database connection."""
    path = db_path or DEFAULT_DB_PATH
    key = f"conn_{path}"

    conn = getattr(_thread_local, key, None)
    if conn is None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path)
        conn.executescript(_SCHEMA)
        setattr(_thread_local, key, conn)
    return conn


def log_call(
    model: str,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
    cost_usd: float | None,
    latency_ms: float,
    endpoint: str = "chat.completions",
    status: str = "ok",
    error: str | None = None,
    metadata: str | None = None,
    db_path: str | None = None,
) -> None:
    """Log a single API call to the database."""
    conn = get_db(db_path)
    conn.execute(
        """INSERT INTO calls
           (timestamp, model, input_tokens, output_tokens, total_tokens,
            cost_usd, latency_ms, endpoint, status, error, metadata)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            time.time(),
            model,
            input_tokens,
            output_tokens,
            total_tokens,
            cost_usd,
            latency_ms,
            endpoint,
            status,
            error,
            metadata,
        ),
    )
    conn.commit()
