from datetime import date, timedelta
from app.models.storage_manager import StorageManager

class CalendarViewModel:
    def __init__(self, storage: StorageManager):
        self.storage = storage

    def get_events_for_month(self, year: int, month: int) -> dict:
        events = {}
        cycles = self.storage.get_all_cycles()
        
        for cycle in cycles:
            start_date = date.fromisoformat(cycle['start_date'])
            # Simplistic end date if none provided (e.g., 5 days)
            end_date = date.fromisoformat(cycle['end_date']) if cycle['end_date'] else start_date + timedelta(days=4)
            
            # Add to events dictionary
            current_date = start_date
            while current_date <= end_date:
                if current_date.year == year and current_date.month == month:
                    events[current_date] = {'type': 'period'}
                current_date += timedelta(days=1)
                
        # Future enhancements: overlay symptoms and predictions
        return events
