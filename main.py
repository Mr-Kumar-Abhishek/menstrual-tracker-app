from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from app.views.main_view import MainView
from app.models.notification_manager import NotificationManager
import app.views.calendar_view
import app.views.log_view

class MenstrualTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"
        
        # Check and send any pending notifications
        try:
            NotificationManager().check_and_send_reminders()
        except Exception as e:
            print("Failed to schedule notifications:", e)

        sm = MDScreenManager()
        main_view = MainView(name='main')
        sm.add_widget(main_view)

        return sm

if __name__ == "__main__":
    MenstrualTrackerApp().run()
