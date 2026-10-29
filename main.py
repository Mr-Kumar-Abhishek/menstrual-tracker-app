import os
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from app.views.main_view import MainView
from app.models.notification_manager import NotificationManager
from app.models.storage_manager import StorageManager


class MenstrualTrackerApp(MDApp):
    def build(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        for icon_file in ("icon.png", "icon.jpg"):
            icon_path = os.path.join(base_dir, icon_file)
            if os.path.exists(icon_path):
                self.icon = icon_path
                break

        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"

        # Initialize encrypted database and check pending notifications
        try:
            storage = StorageManager()
            storage.initialize_database()
            if not storage.get_all_cycles():
                storage.seed_sample_data()
            if storage.get_setting('notifications_enabled', 'True') == 'True':
                NotificationManager().check_and_send_reminders()
        except Exception as e:
            print("Failed to schedule notifications:", e)

        sm = MDScreenManager()
        main_view = MainView(name='main')
        sm.add_widget(main_view)

        return sm


if __name__ == "__main__":
    MenstrualTrackerApp().run()
