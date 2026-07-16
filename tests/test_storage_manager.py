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
    assert "settings" in tables

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

def test_get_active_cycle(storage):
    assert storage.get_active_cycle() is None
    
    storage.add_cycle(start_date=date(2026, 1, 1), end_date=None)
    active = storage.get_active_cycle()
    assert active is not None
    assert active['start_date'] == '2026-01-01'

def test_update_cycle_end_date(storage):
    cycle_id = storage.add_cycle(start_date=date(2026, 1, 1), end_date=None)
    storage.update_cycle_end_date(cycle_id, date(2026, 1, 5))
    
    cycles = storage.get_all_cycles()
    assert cycles[0]['end_date'] == '2026-01-05'
    assert storage.get_active_cycle() is None

def test_settings(storage):
    # Test default
    assert storage.get_setting("nonexistent") is None
    assert storage.get_setting("notifications", "False") == "False"
    
    # Test set and get
    storage.set_setting("notifications", "True")
    assert storage.get_setting("notifications") == "True"
    
    # Test update
    storage.set_setting("notifications", "False")
    assert storage.get_setting("notifications") == "False"

def test_get_all_daily_logs(storage):
    storage.add_daily_log(date(2026, 1, 1), "Light", "None", "Happy", "")
    storage.add_daily_log(date(2026, 1, 2), "Heavy", "Cramps", "Sad", "")
    logs = storage.get_all_daily_logs()
    assert len(logs) == 2
    assert logs[0]['date'] == '2026-01-01'
    assert logs[1]['date'] == '2026-01-02'

def test_export_data(storage, tmp_path):
    storage.add_cycle(start_date=date(2026, 1, 1), end_date=date(2026, 1, 5))
    storage.add_daily_log(date(2026, 1, 1), "Light", "None", "Happy", "Note")
    
    export_file = tmp_path / "export.json"
    storage.export_data(str(export_file))
    
    assert export_file.exists()
    
    import json
    with open(export_file, 'r') as f:
        data = json.load(f)
        
    assert "cycles" in data
    assert "daily_logs" in data
    assert len(data['cycles']) == 1
    assert data['cycles'][0]['start_date'] == '2026-01-01'
    assert len(data['daily_logs']) == 1
    assert data['daily_logs'][0]['notes'] == 'Note'

from unittest.mock import patch

def test_database_fallback_to_memory():
    # Use a path that simulates a read-only or invalid directory
    sm = StorageManager(db_path="/invalid_read_only_dir/test.db")
    
    original_connect = sqlite3.connect
    
    def mock_connect(*args, **kwargs):
        if "/invalid_read_only_dir" in args[0]:
            raise sqlite3.OperationalError("unable to open database file")
        return original_connect(*args, **kwargs)
        
    with patch('sqlite3.connect', side_effect=mock_connect):
        sm.initialize_database()
        
        # Verify fallback activated and path was reassigned
        assert sm._fallback_active is True
        assert sm.db_path == "file:memdb1?mode=memory&cache=shared"
        
        # Verify we can add and retrieve data correctly from the shared memory DB
        cycle_id = sm.add_cycle(start_date=date(2026, 1, 1))
        assert cycle_id is not None
        
        cycles = sm.get_all_cycles()
        assert len(cycles) == 1
        assert cycles[0]['start_date'] == '2026-01-01'
