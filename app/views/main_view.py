import os
import sys
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import NoTransition
# Import all child views so KV lang can resolve them
from app.views.dashboard_view import (  # noqa: F401
    DashboardView,
    strip_widget_elevation_shadow,
)
from app.views.calendar_view import CalendarView    # noqa: F401
from app.views.log_view import LogEntryView         # noqa: F401
from app.views.settings_view import SettingsView    # noqa: F401


def get_system_bottom_inset() -> float:
    """Return safe bottom inset (in pixels) to clear Android Home/Navigation buttons."""
    default_dp = float(os.environ.get("MENSTRUAL_BOTTOM_INSET_DP", "48"))
    inset_px = dp(default_dp)
    if sys.platform == "android" or "ANDROID_ARGUMENT" in os.environ:
        try:
            from jnius import autoclass
            Resources = autoclass("android.content.res.Resources")
            res = Resources.getSystem()
            res_id = res.getIdentifier("navigation_bar_height", "dimen", "android")
            if res_id > 0:
                nav_px = float(res.getDimensionPixelSize(res_id))
                if nav_px > inset_px:
                    inset_px = nav_px
        except Exception:
            pass
    return inset_px


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
    md_bg_color: 0.95, 0.95, 0.96, 1

    MDBottomNavigation:
        id: bottom_nav
        padding: 0, 0, 0, root.bottom_safe_inset
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
    bottom_safe_inset = NumericProperty(0)
    nav_bar_height = NumericProperty(0)

    def __init__(self, **kwargs):
        self.bottom_safe_inset = get_system_bottom_inset()
        self.nav_bar_height = dp(68)
        super().__init__(**kwargs)
        self._top_border_line = None
        self._bottom_border_line = None
        self._safe_area_bg = None
        Window.bind(on_keyboard=self._on_keyboard)
        self._init_views()
        Clock.schedule_once(self._init_views, 0)

    def _on_keyboard(self, window, key, *args):
        """Adapt to Android Back button: return to Dashboard tab before exiting."""
        if key == 27 and "bottom_nav" in self.ids:
            bnav = self.ids.bottom_nav
            if bnav.ids.tab_manager.current != "screen_dashboard":
                bnav.switch_tab("screen_dashboard")
                return True
        return False

    def on_size(self, *args):
        self._sync_bottom_bar()
        Clock.schedule_once(self._sync_bottom_bar, 0)

    def _sync_bottom_bar(self, *args):
        strip_widget_elevation_shadow(self)
        if "bottom_nav" not in self.ids:
            return
        bnav = self.ids.bottom_nav
        try:
            self.bottom_safe_inset = get_system_bottom_inset()
            self.nav_bar_height = dp(68)
            panel = bnav.ids.bottom_panel
            tab_bar = bnav.ids.tab_bar
            panel.height = self.nav_bar_height
            tab_bar.height = self.nav_bar_height
            bnav.on_resize(do_again=False)

            if self._top_border_line is None:
                with panel.canvas.before:
                    Color(0.95, 0.95, 0.96, 1)
                    self._safe_area_bg = Rectangle(
                        pos=(self.x, 0),
                        size=(self.width, self.bottom_safe_inset),
                    )
                with panel.canvas.after:
                    Color(0.86, 0.86, 0.88, 1)
                    self._top_border_line = Line(
                        points=[self.x, panel.top, self.right, panel.top],
                        width=dp(1),
                    )
                    Color(0.90, 0.90, 0.92, 1)
                    self._bottom_border_line = Line(
                        points=[self.x, panel.y, self.right, panel.y],
                        width=dp(1),
                    )
                panel.bind(pos=self._update_border_line, size=self._update_border_line)
            else:
                self._update_border_line()

            for header in tab_bar.children:
                header.height = self.nav_bar_height
                header.padding = (0, dp(10), 0, dp(6))
                header._label_font_size = sp(12)
                lbl = header.ids.get("_label")
                if lbl is not None:
                    lbl.font_size = sp(12)
                    lbl.size_hint_x = 1
                    lbl.halign = "center"
                    lbl.y = dp(0)
        except Exception:
            pass

    def _update_border_line(self, *args):
        if self._top_border_line is not None and "bottom_nav" in self.ids:
            panel = self.ids.bottom_nav.ids.bottom_panel
            right_edge = max(self.right, panel.right)
            self._top_border_line.points = [self.x, panel.top, right_edge, panel.top]
            if self._bottom_border_line is not None:
                self._bottom_border_line.points = [self.x, panel.y, right_edge, panel.y]
            if self._safe_area_bg is not None:
                self._safe_area_bg.pos = (self.x, 0)
                self._safe_area_bg.size = (right_edge, self.bottom_safe_inset)

    def _init_views(self, *args):
        try:
            self.ids.bottom_nav.transition = InstantTabTransition
            self.ids.bottom_nav.ids.tab_manager.transition = InstantTabTransition()
            self._sync_bottom_bar()
        except Exception:
            pass
        if "dashboard_view" in self.ids:
            self.ids.dashboard_view.on_enter()
