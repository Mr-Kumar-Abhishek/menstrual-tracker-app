import pytest
from datetime import date, timedelta
from app.models.storage_manager import StorageManager
from app.viewmodels.dashboard_viewmodel import DashboardViewModel
import sqlite3

@pytest.fixture
def temp_storage(tmp_path):
    db_path = tmp_path / "test.db"
    storage = StorageManager(str(db_path))
    storage.initialize_database()
    return storage

def test_get_current_cycle_day(temp_storage):
    vm = DashboardViewModel(temp_storage)
    assert vm.get_current_cycle_day() == "N/A"
    
    start = date.today() - timedelta(days=5)
    temp_storage.add_cycle(start)
    assert vm.get_current_cycle_day() == "Day 6"

def test_get_next_period_prediction(temp_storage):
    vm = DashboardViewModel(temp_storage)
    assert vm.get_next_period_prediction() == "No prediction available (need more data)"
    
    start = date.today() - timedelta(days=28)
    temp_storage.add_cycle(start, start + timedelta(days=4))
    
    pred = vm.get_next_period_prediction()
    assert "Starts today" in pred

def test_get_ovulation_prediction(temp_storage):
    vm = DashboardViewModel(temp_storage)
    assert vm.get_ovulation_prediction() == "Need more data"
    
    start = date.today() - timedelta(days=28)
    temp_storage.add_cycle(start, start + timedelta(days=4))
    
    pred = vm.get_ovulation_prediction()
    assert "-" in pred
