import os
import tempfile
import pytest
from datetime import date
from app.models.storage_manager import StorageManager
from app.viewmodels.dashboard_viewmodel import DashboardViewModel
from app.viewmodels.calendar_viewmodel import CalendarViewModel

@pytest.fixture
def storage():
    db_fd, db_path = tempfile.mkstemp()
    sm = StorageManager(db_path=db_path)
    sm.initialize_database()
    yield sm
    os.close(db_fd)
    os.unlink(db_path)

def test_dashboard_viewmodel_no_data(storage):
    vm = DashboardViewModel(storage)
    assert vm.get_next_period_prediction() == "No prediction available (need more data)"
    assert vm.get_current_cycle_day() == "N/A"

def test_dashboard_viewmodel_with_data(storage):
    # Log a cycle 10 days ago
    start = date.today()
    start_10_days_ago = date(start.year, start.month, start.day)
    import datetime
    start_10_days_ago = datetime.date.today() - datetime.timedelta(days=10)
    
    storage.add_cycle(start_date=start_10_days_ago, end_date=start_10_days_ago + datetime.timedelta(days=4))
    
    vm = DashboardViewModel(storage)
    prediction = vm.get_next_period_prediction()
    assert "Starts in" in prediction or "Starts on" in prediction
    assert vm.get_current_cycle_day() == "Day 11" # 10 days ago + today = day 11

def test_calendar_viewmodel(storage):
    storage.add_cycle(start_date=date(2026, 1, 1), end_date=date(2026, 1, 5))
    vm = CalendarViewModel(storage)
    
    events = vm.get_events_for_month(2026, 1)
    # Expecting cycle start/end in events
    assert date(2026, 1, 1) in events
    assert events[date(2026, 1, 1)]['type'] == 'period'
