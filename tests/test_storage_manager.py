import os
import sqlite3
import tempfile
import pytest
from datetime import date
from app.models.storage_manager import StorageManager

@pytest.fixture
def storage():
    db_fd, db_path = tempfile.mkstemp()
    sm = StorageManager(db_path=db_path)
    sm.initialize_database()
    yield sm
    os.close(db_fd)
    os.unlink(db_path)

def test_database_initialization(storage):
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

def test_cycle_sorting(storage):
    storage.add_cycle(start_date=date(2026, 3, 1), end_date=date(2026, 3, 5))
    storage.add_cycle(start_date=date(2026, 1, 1), end_date=date(2026, 1, 5))
    storage.add_cycle(start_date=date(2026, 2, 1), end_date=date(2026, 2, 5))
    
    cycles = storage.get_all_cycles()
    assert len(cycles) == 3
    # StorageManager returns DESC
    assert cycles[0]['start_date'] == '2026-03-01'
    assert cycles[1]['start_date'] == '2026-02-01'
    assert cycles[2]['start_date'] == '2026-01-01'

def test_add_and_get_daily_log(storage):
    storage.add_daily_log(
        log_date=date(2026, 1, 2),
        flow_intensity="Heavy",
        symptoms="Cramps",
        mood="Sad",
        notes="Testing"
    )
    logs = storage.get_daily_log(date(2026, 1, 2))
    assert logs['flow_intensity'] == "Heavy"
    
def test_daily_log_overwrite(storage):
    storage.add_daily_log(log_date=date(2026, 1, 2), flow_intensity="Light", symptoms="", mood="Happy")
    storage.add_daily_log(log_date=date(2026, 1, 2), flow_intensity="Heavy", symptoms="Cramps", mood="Sad")
    
    logs = storage.get_daily_log(date(2026, 1, 2))
    assert logs['flow_intensity'] == "Heavy"
    assert logs['mood'] == "Sad"
    assert logs['symptoms'] == "Cramps"

def test_sql_injection_resistance(storage):
    malicious_text = "Heavy', 'Hack'); DROP TABLE daily_logs;--"
    storage.add_daily_log(
        log_date=date(2026, 1, 2),
        flow_intensity=malicious_text,
        symptoms="", mood=""
    )
    logs = storage.get_daily_log(date(2026, 1, 2))
    assert logs['flow_intensity'] == malicious_text
