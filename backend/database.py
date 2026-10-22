import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "router_logs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            prompt TEXT,
            route_taken TEXT,
            complexity_score REAL,
            latency_ms REAL,
            estimated_cost_usd REAL,
            response_preview TEXT,
            cloud_provider TEXT DEFAULT 'none',
            co2_grams REAL DEFAULT 0.0,
            energy_kwh REAL DEFAULT 0.0,
            fallback_reason TEXT DEFAULT NULL,
            classifier_confidence REAL DEFAULT NULL,
            classify_ms REAL DEFAULT NULL,
            inference_ms REAL DEFAULT NULL,
            model_name TEXT DEFAULT NULL
        )
    """)
    conn.commit()

    # Automatic migration: Add missing columns if upgrading an existing database
    cursor.execute("PRAGMA table_info(requests_log)")
    existing_columns = [col[1] for col in cursor.fetchall()]

    if "cloud_provider" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN cloud_provider TEXT DEFAULT 'none'")
    if "co2_grams" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN co2_grams REAL DEFAULT 0.0")
    if "energy_kwh" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN energy_kwh REAL DEFAULT 0.0")
    if "fallback_reason" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN fallback_reason TEXT DEFAULT NULL")
    if "classifier_confidence" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN classifier_confidence REAL DEFAULT NULL")
    if "classify_ms" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN classify_ms REAL DEFAULT NULL")
    if "inference_ms" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN inference_ms REAL DEFAULT NULL")
    if "model_name" not in existing_columns:
        cursor.execute("ALTER TABLE requests_log ADD COLUMN model_name TEXT DEFAULT NULL")

    conn.commit()
    conn.close()

def log_request(
    prompt: str,
    route_taken: str,
    complexity_score: float,
    latency_ms: float,
    estimated_cost_usd: float,
    response_preview: str,
    cloud_provider: str = "none",
    co2_grams: float = 0.0,
    energy_kwh: float = 0.0,
    fallback_reason: str = None,
    classifier_confidence: float = None,
    classify_ms: float = None,
    inference_ms: float = None,
    model_name: str = None
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO requests_log 
        (timestamp, prompt, route_taken, complexity_score, latency_ms, estimated_cost_usd, response_preview, cloud_provider, co2_grams, energy_kwh, fallback_reason, classifier_confidence, classify_ms, inference_ms, model_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        prompt,
        route_taken,
        complexity_score,
        latency_ms,
        estimated_cost_usd,
        response_preview,
        cloud_provider,
        co2_grams,
        energy_kwh,
        fallback_reason,
        classifier_confidence,
        classify_ms,
        inference_ms,
        model_name
    ))
    conn.commit()
    conn.close()

def clear_db():
    """Empties the requests_log table and resets auto-increment ID for demo."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM requests_log")
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='requests_log'")
    except Exception:
        pass
    conn.commit()
    conn.close()

