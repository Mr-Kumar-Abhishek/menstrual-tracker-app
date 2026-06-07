from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from app.views.main_view import MainView
# Ensure child views are loaded
import app.views.calendar_view
import app.views.log_view

class MenstrualTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        main_view = MainView(name='main')
        sm.add_widget(main_view)

        return sm

if __name__ == "__main__":
    MenstrualTrackerApp().run()
