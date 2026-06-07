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
        
        if not next_period:
            return "No prediction available (need more data)"
            
        days_away = (next_period - date.today()).days
        
        if days_away > 0:
            return f"Starts in {days_away} days ({next_period.strftime('%b %d')})"
        elif days_away == 0:
            return "Starts today"
        else:
            return f"Overdue by {abs(days_away)} days"

    def get_current_cycle_day(self) -> str:
        cycles = self.storage.get_all_cycles()
        if not cycles:
            return "N/A"
            
        most_recent_start = date.fromisoformat(cycles[0]['start_date'])
        days_since = (date.today() - most_recent_start).days
        
        if days_since < 0:
            return "N/A"
            
        return f"Day {days_since + 1}"
