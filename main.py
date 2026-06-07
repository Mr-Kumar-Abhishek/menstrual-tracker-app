from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from app.views.dashboard_view import DashboardView

class MenstrualTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        
        dashboard = DashboardView(name='dashboard')
        sm.add_widget(dashboard)

        return sm

if __name__ == "__main__":
    MenstrualTrackerApp().run()
