from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app.views.dashboard_view import DashboardView
# We will import the other views below

KV = '''
<MainView>:
    MDBottomNavigation:
        panel_color: app.theme_cls.bg_normal
        selected_color_background: app.theme_cls.primary_color
        text_color_active: app.theme_cls.primary_color

        MDBottomNavigationItem:
            name: 'screen_dashboard'
            text: 'Dashboard'
            icon: 'view-dashboard'
            
            DashboardView:
                id: dashboard_view

        MDBottomNavigationItem:
            name: 'screen_calendar'
            text: 'Calendar'
            icon: 'calendar-month'
            
            CalendarView:
                id: calendar_view

        MDBottomNavigationItem:
            name: 'screen_log'
            text: 'Log'
            icon: 'plus-circle'
            
            LogEntryView:
                id: log_view
        MDBottomNavigationItem:
            name: 'screen_settings'
            text: 'Settings'
            icon: 'cog'
            
            SettingsView:
                id: settings_view
'''
Builder.load_string(KV)

class MainView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
