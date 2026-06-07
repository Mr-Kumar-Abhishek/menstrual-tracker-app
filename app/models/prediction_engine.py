from datetime import date, timedelta, datetime

class PredictionEngine:
    DEFAULT_CYCLE_LENGTH = 28
    LUTEAL_PHASE_LENGTH = 14

    def __init__(self, historical_cycles: list[dict]):
        self.historical_cycles = sorted(
            historical_cycles,
            key=lambda c: datetime.strptime(c['start_date'], '%Y-%m-%d').date()
        )

    def _get_average_cycle_length(self) -> int:
        if len(self.historical_cycles) < 2:
            return self.DEFAULT_CYCLE_LENGTH
        
        total_days = 0
        intervals = len(self.historical_cycles) - 1
        
        for i in range(intervals):
            date1 = datetime.strptime(self.historical_cycles[i]['start_date'], '%Y-%m-%d').date()
            date2 = datetime.strptime(self.historical_cycles[i+1]['start_date'], '%Y-%m-%d').date()
            total_days += (date2 - date1).days
            
        return max(21, min(35, round(total_days / intervals)))

    def predict_next_period(self) -> date | None:
        if not self.historical_cycles:
            return None
        
        most_recent_start = datetime.strptime(
            self.historical_cycles[-1]['start_date'], '%Y-%m-%d'
        ).date()
        
        avg_length = self._get_average_cycle_length()
        return most_recent_start + timedelta(days=avg_length)

    def predict_ovulation_window(self) -> tuple[date, date] | tuple[None, None]:
        next_period = self.predict_next_period()
        if not next_period:
            return None, None
            
        ovulation_day = next_period - timedelta(days=self.LUTEAL_PHASE_LENGTH)
        # Ovulation window is typically 5 days (4 days before ovulation to day of)
        # Here we'll return a 5 day window centered slightly before the ovulation day
        start_window = ovulation_day - timedelta(days=2)
        end_window = ovulation_day + timedelta(days=2)
        
        return start_window, end_window
