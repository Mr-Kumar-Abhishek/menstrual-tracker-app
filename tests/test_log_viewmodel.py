import pytest
from datetime import date, timedelta
from app.models.storage_manager import StorageManager
from app.viewmodels.log_viewmodel import LogViewModel
import tempfile
import os

@pytest.fixture
def storage():
    db_fd, db_path = tempfile.mkstemp()
    sm = StorageManager(db_path=db_path)
    sm.initialize_database()
    yield sm
    os.close(db_fd)
    os.unlink(db_path)

def test_start_period(storage):
    vm = LogViewModel(storage)
    assert not vm.is_period_active()
    
    vm.start_period(date(2026, 1, 1))
    assert vm.is_period_active()
    active = storage.get_active_cycle()
    assert active['start_date'] == '2026-01-01'
    
    # Starting a new period while one is active should end the previous one
    vm.start_period(date(2026, 2, 1))
    cycles = storage.get_all_cycles()
    assert len(cycles) == 2
    # The previous one should be ended on the day before the new one
    assert cycles[1]['end_date'] == '2026-01-31'
    assert cycles[0]['start_date'] == '2026-02-01'

def test_end_period(storage):
    vm = LogViewModel(storage)
    vm.start_period(date(2026, 1, 1))
    vm.end_period(date(2026, 1, 5))
    
    assert not vm.is_period_active()
    cycles = storage.get_all_cycles()
    assert cycles[0]['end_date'] == '2026-01-05'

def test_save_log(storage):
    vm = LogViewModel(storage)
    vm.save_daily_log(date(2026, 1, 2), "Heavy", "Cramps", "Sad")
    log = storage.get_daily_log(date(2026, 1, 2))
    assert log['flow_intensity'] == "Heavy"
