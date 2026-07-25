from datetime import date, timedelta
from app.models.storage_manager import StorageManager
from app.models.prediction_engine import PredictionEngine


class CalendarViewModel:
    def __init__(self, storage: StorageManager):
        self.storage = storage

    def get_events_for_month(self, year: int, month: int) -> dict:
        events = {}
        cycles = self.storage.get_all_cycles()

        # Add historical cycles
        for cycle in cycles:
            start_date = date.fromisoformat(cycle['start_date'])
            end_date = date.fromisoformat(
                cycle['end_date']) if cycle['end_date'] else start_date + timedelta(days=4)

            current_date = start_date
            while current_date <= end_date:
                if current_date.year == year and current_date.month == month:
                    events[current_date] = {'type': 'period'}
                current_date += timedelta(days=1)

        # Predictions
        if cycles:
            engine = PredictionEngine(cycles)
            next_period = engine.predict_next_period()

            if next_period and next_period.year == year and next_period.month == month:
                # Highlight 5 days as predicted period
                for i in range(5):
                    d = next_period + timedelta(days=i)
                    if d.year == year and d.month == month and d not in events:
                        events[d] = {'type': 'predicted_period'}

            start_ov, end_ov = engine.predict_ovulation_window()
            if start_ov and end_ov:
                curr = start_ov
                while curr <= end_ov:
                    if curr.year == year and curr.month == month and curr not in events:
                        events[curr] = {'type': 'predicted_ovulation'}
                    curr += timedelta(days=1)

        # Add logged symptoms
        logs = self.storage.get_all_daily_logs()
        for log in logs:
            log_date = date.fromisoformat(log['date'])
            if log_date.year == year and log_date.month == month:
                if log_date not in events:
                    events[log_date] = {'type': 'none'}
                events[log_date]['has_symptoms'] = True

        return events
