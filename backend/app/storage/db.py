import sqlite3
import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

def get_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str) -> None:
    # Crear el directorio si no existe
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        run_id TEXT PRIMARY KEY,
        periodo TEXT NOT NULL,
        created_at TEXT NOT NULL,
        output_json TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_run(db_path: str, run_id: str, periodo: str, output: Dict[str, Any]) -> None:
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO runs(run_id, periodo, created_at, output_json) VALUES (?, ?, ?, ?)",
        (run_id, periodo, datetime.utcnow().isoformat() + "Z", json.dumps(output, ensure_ascii=False))
    )
    conn.commit()
    conn.close()

def get_latest_run(db_path: str) -> Optional[Dict[str, Any]]:
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM runs ORDER BY created_at DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return json.loads(row["output_json"])

def list_runs(db_path: str, limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("SELECT run_id, periodo, created_at FROM runs ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_run(db_path: str, run_id: str) -> Optional[Dict[str, Any]]:
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return json.loads(row["output_json"])

