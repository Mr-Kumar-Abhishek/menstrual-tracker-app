from datetime import date, timedelta
from app.models.storage_manager import StorageManager

class LogViewModel:
    def __init__(self, storage: StorageManager):
        self.storage = storage

    def is_period_active(self) -> bool:
        return self.storage.get_active_cycle() is not None

    def start_period(self, start_date: date):
        active_cycle = self.storage.get_active_cycle()
        if active_cycle:
            end_date = start_date - timedelta(days=1)
            if end_date < date.fromisoformat(active_cycle['start_date']):
                end_date = date.fromisoformat(active_cycle['start_date'])
            self.storage.update_cycle_end_date(active_cycle['cycle_id'], end_date)
            
        self.storage.add_cycle(start_date=start_date, end_date=None)

    def end_period(self, end_date: date):
        active_cycle = self.storage.get_active_cycle()
        if active_cycle:
            self.storage.update_cycle_end_date(active_cycle['cycle_id'], end_date)

    def save_daily_log(self, log_date: date, flow: str, symptoms: str, mood: str, notes: str = ""):
        self.storage.add_daily_log(
            log_date=log_date,
            flow_intensity=flow,
            symptoms=symptoms,
            mood=mood,
            notes=notes
        )
