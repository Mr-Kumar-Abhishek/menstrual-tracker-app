import os
import tempfile
import pytest
from datetime import date, timedelta
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

def test_dashboard_no_data(storage):
    vm = DashboardViewModel(storage)
    assert vm.get_next_period_prediction() == "No prediction available (need more data)"
    assert vm.get_current_cycle_day() == "N/A"

def test_dashboard_cycle_day_calculation(storage):
    # Period started today -> Day 1
    storage.add_cycle(start_date=date.today(), end_date=None)
    vm = DashboardViewModel(storage)
    assert vm.get_current_cycle_day() == "Day 1"

def test_dashboard_prediction_formatting(storage):
    start = date.today() - timedelta(days=28)
    storage.add_cycle(start_date=start, end_date=None)
    vm = DashboardViewModel(storage)
    pred = vm.get_next_period_prediction()
    assert "Starts today" in pred or "Starts in" in pred

def test_calendar_month_spanning_events(storage):
    # Period crossing month boundary: Jan 28 to Feb 2
    storage.add_cycle(start_date=date(2026, 1, 28), end_date=date(2026, 2, 2))
    vm = CalendarViewModel(storage)
    
    jan_events = vm.get_events_for_month(2026, 1)
    feb_events = vm.get_events_for_month(2026, 2)
    
    assert date(2026, 1, 28) in jan_events
    assert date(2026, 1, 31) in jan_events
    assert date(2026, 2, 1) in feb_events
    assert date(2026, 2, 2) in feb_events
    assert date(2026, 2, 3) not in feb_events

def test_calendar_prediction_generation(storage):
    storage.add_cycle(start_date=date(2026, 1, 1), end_date=date(2026, 1, 5))
    vm = CalendarViewModel(storage)
    
    # 28 days later is Jan 29
    jan_events = vm.get_events_for_month(2026, 1)
    
    # Actual period
    assert jan_events[date(2026, 1, 1)]['type'] == 'period'
    
    # Predicted period (Jan 29 to Feb 2)
    assert date(2026, 1, 29) in jan_events
    assert jan_events[date(2026, 1, 29)]['type'] == 'predicted_period'
    
    # Predicted ovulation (14 days before Jan 29 = Jan 15)
    assert date(2026, 1, 15) in jan_events
    assert jan_events[date(2026, 1, 15)]['type'] == 'predicted_ovulation'
