import pytest
from datetime import date, timedelta
from app.models.prediction_engine import PredictionEngine

def test_prediction_no_history():
    engine = PredictionEngine(historical_cycles=[])
    assert engine.predict_next_period() is None

def test_prediction_single_cycle():
    cycles = [{'start_date': '2026-01-01', 'end_date': '2026-01-05', 'cycle_length': None}]
    engine = PredictionEngine(historical_cycles=cycles)
    next_period = engine.predict_next_period()
    # Default 28 days
    assert next_period == date(2026, 1, 1) + timedelta(days=28)

def test_prediction_multiple_cycles():
    # Cycle 1: 30 days
    # Cycle 2: 26 days
    # Average: 28 days
    cycles = [
        {'start_date': '2026-03-02', 'end_date': '2026-03-06'}, # Most recent
        {'start_date': '2026-01-31', 'end_date': '2026-02-04'},
        {'start_date': '2026-01-01', 'end_date': '2026-01-05'}
    ]
    engine = PredictionEngine(historical_cycles=cycles)
    next_period = engine.predict_next_period()
    # Average of differences between start dates:
    # 2026-01-01 to 2026-01-31 = 30 days
    # 2026-01-31 to 2026-03-02 = 30 days
    # (Note: 2026 is not a leap year, so Jan 31 + 30 days = March 2)
    # Average length = 30 days
    assert next_period == date(2026, 3, 2) + timedelta(days=30)

def test_ovulation_window():
    cycles = [{'start_date': '2026-03-02', 'end_date': '2026-03-06'}]
    engine = PredictionEngine(historical_cycles=cycles)
    ovulation_start, ovulation_end = engine.predict_ovulation_window()
    # Next period starts March 30. Ovulation ~14 days before = March 16. Window = 14 to 18.
    assert ovulation_start == date(2026, 3, 14)
    assert ovulation_end == date(2026, 3, 18)
