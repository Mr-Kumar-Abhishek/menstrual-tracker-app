from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.metrics import dp, sp
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
        panel_color: 1, 1, 1, 1
        selected_color_background: app.theme_cls.primary_color[:3] + [0.18]
        text_color_active: app.theme_cls.primary_color
        text_color_normal: 0.42, 0.42, 0.46, 1

        MDBottomNavigationItem:
            name: 'screen_dashboard'
            text: 'Dashboard'
            icon: 'view-dashboard'
            on_tab_press:
                root._sync_bottom_bar()
                dashboard_view.on_enter()

            DashboardView:
                id: dashboard_view

        MDBottomNavigationItem:
            name: 'screen_calendar'
            text: 'Calendar'
            icon: 'calendar-month'
            on_tab_press:
                root._sync_bottom_bar()
                calendar_view.on_enter()

            CalendarView:
                id: calendar_view

        MDBottomNavigationItem:
            name: 'screen_log'
            text: 'Log'
            icon: 'plus-circle'
            on_tab_press: root._sync_bottom_bar()

            LogEntryView:
                id: log_view

        MDBottomNavigationItem:
            name: 'screen_settings'
            text: 'Settings'
            icon: 'cog'
            on_tab_press:
                root._sync_bottom_bar()
                settings_view.on_enter()

            SettingsView:
                id: settings_view
'''
Builder.load_string(KV)


class MainView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._border_line = None
        self._init_views()
        Clock.schedule_once(self._init_views, 0)

    def on_size(self, *args):
        self._sync_bottom_bar()
        Clock.schedule_once(self._sync_bottom_bar, 0)

    def _sync_bottom_bar(self, *args):
        if "bottom_nav" not in self.ids:
            return
        bnav = self.ids.bottom_nav
        try:
            bnav.on_resize(do_again=False)
            panel = bnav.ids.bottom_panel
            if self._border_line is None:
                with panel.canvas.after:
                    Color(0.86, 0.86, 0.88, 1)
                    self._border_line = Line(
                        points=[self.x, panel.top, self.right, panel.top],
                        width=dp(1),
                    )
                panel.bind(pos=self._update_border_line, size=self._update_border_line)
            else:
                self._update_border_line()

            for header in bnav.ids.tab_bar.children:
                header.padding = (0, dp(15), 0, dp(12))
                header._label_font_size = sp(12)
                lbl = header.ids.get("_label")
                if lbl is not None:
                    lbl.font_size = sp(12)
                    lbl.size_hint_x = 1
                    lbl.halign = "center"
                    lbl.y = dp(2)
        except Exception:
            pass

    def _update_border_line(self, *args):
        if self._border_line is not None and "bottom_nav" in self.ids:
            panel = self.ids.bottom_nav.ids.bottom_panel
            right_edge = max(self.right, panel.right)
            self._border_line.points = [self.x, panel.top, right_edge, panel.top]

    def _init_views(self, *args):
        try:
            self.ids.bottom_nav.transition = InstantTabTransition
            self.ids.bottom_nav.ids.tab_manager.transition = InstantTabTransition()
            self._sync_bottom_bar()
        except Exception:
            pass
        if "dashboard_view" in self.ids:
            self.ids.dashboard_view.on_enter()
