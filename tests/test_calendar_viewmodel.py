import pytest
from datetime import date, timedelta
from app.models.storage_manager import StorageManager
from app.viewmodels.calendar_viewmodel import CalendarViewModel


@pytest.fixture
def temp_storage(tmp_path):
    db_path = tmp_path / "test.db"
    storage = StorageManager(str(db_path))
    storage.initialize_database()
    return storage


def test_get_events_for_month_empty(temp_storage):
    vm = CalendarViewModel(temp_storage)
    events = vm.get_events_for_month(2023, 1)
    assert len(events) == 0


def test_get_events_for_month_with_data(temp_storage):
    vm = CalendarViewModel(temp_storage)

    start = date(2023, 1, 1)
    temp_storage.add_cycle(start, start + timedelta(days=3))

    temp_storage.add_daily_log(
        date(2023, 1, 2), "Heavy", "Cramps", "Neutral", "")

    events = vm.get_events_for_month(2023, 1)

    assert date(2023, 1, 1) in events
    assert events[date(2023, 1, 1)]['type'] == 'period'

    assert date(2023, 1, 2) in events
    assert events[date(2023, 1, 2)]['has_symptoms'] is True

    assert date(2023, 1, 29) in events
    assert events[date(2023, 1, 29)]['type'] == 'predicted_period'

    assert date(2023, 1, 15) in events
    assert events[date(2023, 1, 15)]['type'] == 'predicted_ovulation'
