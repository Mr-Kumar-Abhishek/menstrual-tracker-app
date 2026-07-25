from datetime import date, timedelta
from app.models.prediction_engine import PredictionEngine


def test_prediction_no_history():
    engine = PredictionEngine(historical_cycles=[])
    assert engine.predict_next_period() is None
    assert engine.predict_ovulation_window() == (None, None)


def test_prediction_single_cycle():
    cycles = [{'start_date': '2026-01-01',
               'end_date': '2026-01-05', 'cycle_length': None}]
    engine = PredictionEngine(historical_cycles=cycles)
    next_period = engine.predict_next_period()
    assert next_period == date(2026, 1, 1) + timedelta(days=28)


def test_prediction_multiple_cycles_avg():
    cycles = [
        {'start_date': '2026-03-02', 'end_date': '2026-03-06'},
        {'start_date': '2026-01-31', 'end_date': '2026-02-04'},
        {'start_date': '2026-01-01', 'end_date': '2026-01-05'}
    ]
    engine = PredictionEngine(historical_cycles=cycles)
    next_period = engine.predict_next_period()
    assert next_period == date(2026, 3, 2) + timedelta(days=30)


def test_ovulation_window():
    cycles = [{'start_date': '2026-03-02', 'end_date': '2026-03-06'}]
    engine = PredictionEngine(historical_cycles=cycles)
    ovulation_start, ovulation_end = engine.predict_ovulation_window()
    assert ovulation_start == date(2026, 3, 14)
    assert ovulation_end == date(2026, 3, 18)


def test_prediction_capping_max_length():
    # Gap of 50 days (should cap at 35)
    cycles = [
        {'start_date': '2026-01-01', 'end_date': '2026-01-05'},
        {'start_date': '2026-02-20', 'end_date': '2026-02-25'}  # 50 days later
    ]
    engine = PredictionEngine(historical_cycles=cycles)
    next_period = engine.predict_next_period()
    # Should be 35 days after 2026-02-20
    assert next_period == date(2026, 2, 20) + timedelta(days=35)


def test_prediction_capping_min_length():
    # Gap of 10 days (should cap at 21)
    cycles = [
        {'start_date': '2026-01-01', 'end_date': '2026-01-05'},
        {'start_date': '2026-01-11', 'end_date': '2026-01-15'}  # 10 days later
    ]
    engine = PredictionEngine(historical_cycles=cycles)
    next_period = engine.predict_next_period()
    # Should be 21 days after 2026-01-11
    assert next_period == date(2026, 1, 11) + timedelta(days=21)


def test_missing_end_date():
    # Even without end_date, prediction should work based on start_date
    cycles = [{'start_date': '2026-01-01',
               'end_date': None, 'cycle_length': None}]
    engine = PredictionEngine(historical_cycles=cycles)
    next_period = engine.predict_next_period()
    assert next_period == date(2026, 1, 1) + timedelta(days=28)


def test_prediction_end_date():
    cycles = [
        {'start_date': '2026-03-01', 'end_date': '2026-03-05'},  # 5 days
        {'start_date': '2026-01-31', 'end_date': '2026-02-04'},  # 5 days
        {'start_date': '2026-01-01', 'end_date': '2026-01-08'}  # 8 days
    ]
    # avg duration = (5+5+8)/3 = 6
    engine = PredictionEngine(historical_cycles=cycles)
    start_date = engine.predict_next_period()
    end_date = engine.predict_next_period_end_date()
    assert end_date == start_date + timedelta(days=6 - 1)


def test_prediction_end_date_no_history():
    engine = PredictionEngine(historical_cycles=[])
    assert engine.predict_next_period_end_date() is None


def test_prediction_end_date_no_end_dates():
    cycles = [{'start_date': '2026-01-01',
               'end_date': None, 'cycle_length': None}]
    engine = PredictionEngine(historical_cycles=cycles)
    start_date = engine.predict_next_period()
    end_date = engine.predict_next_period_end_date()
    # default period duration is 5 days (so start_date + 4)
    assert end_date == start_date + timedelta(days=4)
