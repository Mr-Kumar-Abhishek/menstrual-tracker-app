from datetime import date
from app.models.storage_manager import StorageManager
from app.models.prediction_engine import PredictionEngine

class DashboardViewModel:
    def __init__(self, storage: StorageManager):
        self.storage = storage

    def _get_engine(self):
        cycles = self.storage.get_all_cycles()
        return PredictionEngine(cycles)

    def get_next_period_prediction(self) -> str:
        engine = self._get_engine()
        next_period = engine.predict_next_period()
        end_date = engine.predict_next_period_end_date()
        
        if not next_period:
            return "No prediction available (need more data)"
            
        days_away = (next_period - date.today()).days
        
        date_str = f"{next_period.strftime('%b %d')}"
        if end_date:
            date_str += f" - {end_date.strftime('%b %d')}"
        
        if days_away > 0:
            return f"Starts in {days_away} days ({date_str})"
        elif days_away == 0:
            return f"Starts today ({date_str})"
        else:
            return f"Overdue by {abs(days_away)} days ({date_str})"

    def get_ovulation_prediction(self) -> str:
        engine = self._get_engine()
        start_ov, end_ov = engine.predict_ovulation_window()
        
        if not start_ov or not end_ov:
            return "Need more data"
            
        return f"{start_ov.strftime('%b %d')} - {end_ov.strftime('%b %d')}"

    def get_current_cycle_day(self) -> str:
        cycles = self.storage.get_all_cycles()
        if not cycles:
            return "N/A"
            
        most_recent_start = date.fromisoformat(cycles[0]['start_date'])
        days_since = (date.today() - most_recent_start).days
        
        if days_since < 0:
            return "N/A"
            
        return f"Day {days_since + 1}"
