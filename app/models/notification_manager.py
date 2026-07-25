from plyer import notification
from datetime import date
from app.models.storage_manager import StorageManager
from app.models.prediction_engine import PredictionEngine


class NotificationManager:
    def __init__(self):
        self.storage = StorageManager()
        self.engine = PredictionEngine(self.storage.get_all_cycles())

    def check_and_send_reminders(self):
        next_period = self.engine.predict_next_period()
        if not next_period:
            return

        days_away = (next_period - date.today()).days

        if days_away == 2:
            self._send_notification(
                "Upcoming Period",
                "Your next period is predicted to start in 2 days."
            )
        elif days_away == 0:
            self._send_notification(
                "Period Starts Today",
                "Your period is predicted to start today. Remember to log your symptoms!"
            )

    def _send_notification(self, title: str, message: str):
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Menstrual Tracker",
                timeout=10
            )
        except NotImplementedError:
            # Notifications not supported on this platform without extra setup
            print(f"NOTIFICATION: {title} - {message}")
