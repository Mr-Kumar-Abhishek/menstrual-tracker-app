import os
import sqlite3
import tempfile
import pytest
from datetime import date
from app.models.storage_manager import StorageManager

@pytest.fixture
def storage():
    # Use a temporary file for the database during tests
    db_fd, db_path = tempfile.mkstemp()
    sm = StorageManager(db_path=db_path)
    sm.initialize_database()
    yield sm
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

def test_database_initialization(storage):
    # Verify tables are created
    conn = sqlite3.connect(storage.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    assert "cycles" in tables
    assert "daily_logs" in tables

def test_add_and_get_cycle(storage):
    cycle_id = storage.add_cycle(start_date=date(2026, 1, 1), end_date=date(2026, 1, 5))
    assert cycle_id is not None
    
    cycles = storage.get_all_cycles()
    assert len(cycles) == 1
    assert cycles[0]['start_date'] == '2026-01-01'
    assert cycles[0]['end_date'] == '2026-01-05'
    assert cycles[0]['cycle_length'] is None

def test_add_and_get_daily_log(storage):
    log_id = storage.add_daily_log(
        log_date=date(2026, 1, 2),
        flow_intensity="Heavy",
        symptoms="['Cramps', 'Headache']",
        mood="Sad",
        notes="Feeling unwell"
    )
    assert log_id is not None

    logs = storage.get_daily_log(date(2026, 1, 2))
    assert isinstance(logs, dict)
    assert logs['flow_intensity'] == "Heavy"
    assert logs['mood'] == "Sad"
