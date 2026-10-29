from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition
# Import all child views so KV lang can resolve them
from app.views.dashboard_view import DashboardView  # noqa: F401
from app.views.calendar_view import CalendarView    # noqa: F401
from app.views.log_view import LogEntryView         # noqa: F401
from app.views.settings_view import SettingsView    # noqa: F401


class InstantTabTransition(NoTransition):
    """Transition that positions the incoming tab screen immediately without FBO shaders."""

    def __init__(self, **kwargs):
        kwargs["duration"] = 0
        super().__init__(**kwargs)

    def start(self, manager):
        if self.screen_in is not None:
            self.screen_in.pos = manager.pos
            self.screen_in.size = manager.size
        super().start(manager)


KV = '''
<MainView>:
    MDBottomNavigation:
        id: bottom_nav
        panel_color: app.theme_cls.bg_normal
        selected_color_background: app.theme_cls.primary_color[:3] + [0.18]
        text_color_active: app.theme_cls.primary_color

        MDBottomNavigationItem:
            name: 'screen_dashboard'
            text: 'Dashboard'
            icon: 'view-dashboard'
            on_tab_press: dashboard_view.on_enter()

            DashboardView:
                id: dashboard_view

        MDBottomNavigationItem:
            name: 'screen_calendar'
            text: 'Calendar'
            icon: 'calendar-month'
            on_tab_press: calendar_view.on_enter()

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
            on_tab_press: settings_view.on_enter()

            SettingsView:
                id: settings_view
'''
Builder.load_string(KV)


class MainView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_views()
        Clock.schedule_once(self._init_views, 0)

    def _init_views(self, *args):
        try:
            self.ids.bottom_nav.transition = InstantTabTransition
            self.ids.bottom_nav.ids.tab_manager.transition = InstantTabTransition()
        except Exception:
            pass
        if "dashboard_view" in self.ids:
            self.ids.dashboard_view.on_enter()
