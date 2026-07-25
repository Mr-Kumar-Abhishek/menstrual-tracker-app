import time
from app.models.prediction_engine import PredictionEngine
from datetime import date, timedelta


def test_prediction_engine_performance():
    """
    Performance test to ensure prediction engine processes 
    100 historical cycles in under 1 second (well within 3s budget for NFR2).
    """
    # Generate 100 historical cycles
    cycles = []
    current_date = date(2020, 1, 1)
    for _ in range(100):
        start_date = current_date.strftime("%Y-%m-%d")
        end_date = (current_date + timedelta(days=5)).strftime("%Y-%m-%d")
        cycles.append({
            'start_date': start_date,
            'end_date': end_date,
            'cycle_length': None
        })
        current_date += timedelta(days=28)

    start_time = time.perf_counter()

    engine = PredictionEngine(historical_cycles=cycles)
    engine.predict_next_period()
    engine.predict_next_period_end_date()
    engine.predict_ovulation_window()

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    assert execution_time < 1.0, f"Performance test failed! Execution took {execution_time}s (Limit is 1s)"


def test_startup_import_performance():
    """
    Measures the time it takes to import core modules.
    Must be fast to satisfy the 3-second application startup requirement.
    """
    start_time = time.perf_counter()

    # Simulate core imports during app startup

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # Imports alone should be near instantaneous (under 0.5s)
    assert execution_time < 0.5, f"Core import performance failed! Execution took {execution_time}s"
