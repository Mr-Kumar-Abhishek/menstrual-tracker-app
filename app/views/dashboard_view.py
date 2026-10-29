from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton  # noqa: F401
from kivymd.uix.behaviors import CommonElevationBehavior
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from app.viewmodels.dashboard_viewmodel import DashboardViewModel
from app.models.storage_manager import StorageManager


def _clean_single_elevation_widget(w) -> None:
    try:
        w._elevation = 0
        if hasattr(w, "_default_elevation"):
            w._default_elevation = 0
        if hasattr(w, "_elevation_raised"):
            w._elevation_raised = 0
        if hasattr(w, "_anim_raised"):
            w._anim_raised = None
        w._shadow_color = [0.0, 0.0, 0.0, 0.0]
        if hasattr(w, "rect") and w.rect is not None:
            w.rect.size = (0, 0)
        if hasattr(w, "context") and w.context is not None:
            w.context["shadow_color"] = [0.0, 0.0, 0.0, 0.0]
    except Exception:
        pass


if hasattr(CommonElevationBehavior, "set_shader_string"):
    # Patch KivyMD 1.1.x CommonElevationBehavior methods with matching __name__
    # (required by Kivy's WeakMethod in Clock.schedule_once / Window.bind) so
    # its custom GLSL RenderContext never renders a black shadow quad in ScrollView.
    def set_shader_string(self, *args, **kwargs):
        _clean_single_elevation_widget(self)

    def on_elevation(self, *args, **kwargs):
        _clean_single_elevation_widget(self)

    def on_shadow_color(self, *args, **kwargs):
        _clean_single_elevation_widget(self)

    def on_pos(self, *args, **kwargs):
        _clean_single_elevation_widget(self)

    def on_size(self, *args, **kwargs):
        _clean_single_elevation_widget(self)

    def hide_elevation(self, *args, **kwargs):
        _clean_single_elevation_widget(self)

    CommonElevationBehavior.set_shader_string = set_shader_string
    CommonElevationBehavior.on_elevation = on_elevation
    CommonElevationBehavior.on_shadow_color = on_shadow_color
    CommonElevationBehavior.on_pos = on_pos
    CommonElevationBehavior.on_size = on_size
    CommonElevationBehavior.hide_elevation = hide_elevation


def strip_widget_elevation_shadow(widget) -> None:
    """Disable KivyMD CommonElevationBehavior GLSL/BoxShadow artifacts on a widget tree."""
    for w in widget.walk(restrict=True):
        if isinstance(w, CommonElevationBehavior) or hasattr(w, "shadow_color"):
            try:
                if getattr(w, "elevation", 0) != 0:
                    w.elevation = 0
                w.shadow_color = [0.0, 0.0, 0.0, 0.0]
            except Exception:
                pass
            _clean_single_elevation_widget(w)
    Clock.schedule_once(lambda dt: _deferred_strip(widget), 0)


def _deferred_strip(widget) -> None:
    for w in widget.walk(restrict=True):
        if isinstance(w, CommonElevationBehavior) or hasattr(w, "shadow_color"):
            _clean_single_elevation_widget(w)


KV = '''
#:import ScrollEffect kivy.effects.scroll.ScrollEffect

<DashboardView>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_normal

        # ── Header ──────────────────────────────────────────────
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: "100dp"
            padding: "20dp", "16dp"
            md_bg_color: app.theme_cls.primary_color

            MDLabel:
                text: "My Cycle"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                bold: True

            MDLabel:
                id: header_subtitle
                text: ""
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.8

        # ── Empty-state panel (shown when no data) ──────────────
        MDBoxLayout:
            id: empty_state
            orientation: 'vertical'
            padding: "32dp"
            spacing: "14dp"
            size_hint_y: None
            height: "400dp"
            opacity: 0

            AnchorLayout:
                size_hint_y: None
                height: "84dp"

                MDIcon:
                    icon: "calendar-heart"
                    halign: "center"
                    font_size: "72sp"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color[:3] + [0.35]

            MDLabel:
                text: "Welcome to your cycle tracker!"
                font_style: "H6"
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "Log your first period to unlock predictions for your next cycle, ovulation window, and personalised insights."
                halign: "center"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: self.texture_size[1]

            MDRaisedButton:
                text: "Log First Period"
                pos_hint: {"center_x": 0.5}
                elevation: 0
                shadow_color: 0, 0, 0, 0
                md_bg_color: app.theme_cls.primary_color
                on_release: root.go_to_log()

            MDFlatButton:
                text: "Load Sample Data"
                pos_hint: {"center_x": 0.5}
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                on_release: root.load_sample_data()

        # ── Data cards (shown when data exists) ─────────────────
        ScrollView:
            id: data_panel
            opacity: 0
            effect_cls: ScrollEffect
            always_overscroll: False
            bar_width: "3dp"
            bar_color: app.theme_cls.primary_color[:3] + [0.25]
            bar_inactive_color: 0, 0, 0, 0

            MDBoxLayout:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "12dp"
                adaptive_height: True
                md_bg_color: app.theme_cls.bg_normal

                # Current Cycle card
                MDCard:
                    orientation: "horizontal"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint: 1, None
                    height: "90dp"
                    elevation: 0
                    shadow_color: 0, 0, 0, 0
                    md_bg_color: 1, 1, 1, 1
                    line_color: 0.88, 0.88, 0.91, 1
                    radius: [12,]

                    AnchorLayout:
                        size_hint_x: None
                        width: "44dp"

                        MDIcon:
                            icon: "calendar-today"
                            halign: "center"
                            font_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primary_color

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "4dp"
                        pos_hint: {"center_y": 0.5}
                        adaptive_height: True

                        MDLabel:
                            text: "Current Cycle"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            id: current_cycle_label
                            text: ""
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: self.texture_size[1]

                # Next Period card
                MDCard:
                    orientation: "horizontal"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint: 1, None
                    height: "90dp"
                    elevation: 0
                    shadow_color: 0, 0, 0, 0
                    md_bg_color: 1, 1, 1, 1
                    line_color: 0.88, 0.88, 0.91, 1
                    radius: [12,]

                    AnchorLayout:
                        size_hint_x: None
                        width: "44dp"

                        MDIcon:
                            icon: "water"
                            halign: "center"
                            font_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: 0.85, 0.15, 0.45, 1

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "4dp"
                        pos_hint: {"center_y": 0.5}
                        adaptive_height: True

                        MDLabel:
                            text: "Next Period"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            id: prediction_label
                            text: ""
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: self.texture_size[1]

                # Ovulation card
                MDCard:
                    orientation: "horizontal"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint: 1, None
                    height: "90dp"
                    elevation: 0
                    shadow_color: 0, 0, 0, 0
                    md_bg_color: 1, 1, 1, 1
                    line_color: 0.88, 0.88, 0.91, 1
                    radius: [12,]

                    AnchorLayout:
                        size_hint_x: None
                        width: "44dp"

                        MDIcon:
                            icon: "star-circle"
                            halign: "center"
                            font_size: "36sp"
                            theme_text_color: "Custom"
                            text_color: 0.98, 0.6, 0.1, 1

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "4dp"
                        pos_hint: {"center_y": 0.5}
                        adaptive_height: True

                        MDLabel:
                            text: "Ovulation Window"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            id: ovulation_label
                            text: ""
                            font_style: "H6"
                            bold: True
                            size_hint_y: None
                            height: self.texture_size[1]

                # Tip card
                MDCard:
                    orientation: "horizontal"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint: 1, None
                    height: "80dp"
                    elevation: 0
                    shadow_color: 0, 0, 0, 0
                    md_bg_color: 0.96, 0.88, 0.92, 1
                    radius: [12,]

                    AnchorLayout:
                        size_hint_x: None
                        width: "40dp"

                        MDIcon:
                            id: tip_icon
                            icon: "lightbulb-on-outline"
                            halign: "center"
                            font_size: "28sp"
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primary_color

                    MDLabel:
                        id: tip_label
                        text: ""
                        font_style: "Caption"
                        theme_text_color: "Secondary"
                        text_size: self.width, None
                        valign: "middle"

                Widget:
                    size_hint_y: None
                    height: "8dp"
'''
Builder.load_string(KV)


class DashboardView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.storage.initialize_database()
        self.viewmodel = DashboardViewModel(self.storage)
        strip_widget_elevation_shadow(self)
        Clock.schedule_once(lambda dt: self._refresh(), 0)

    def on_enter(self, *args):
        self._refresh()

    def _refresh(self):
        strip_widget_elevation_shadow(self)
        if "empty_state" not in self.ids:
            return
        try:
            cycles = self.storage.get_all_cycles()
            has_data = bool(cycles)

            if not has_data:
                # Show empty / onboarding state
                self.ids.empty_state.opacity = 1
                self.ids.empty_state.disabled = False
                self.ids.empty_state.height = dp(400)
                self.ids.empty_state.padding = dp(32)
                self.ids.empty_state.spacing = dp(14)
                self.ids.data_panel.opacity = 0
                self.ids.data_panel.disabled = True
                self.ids.header_subtitle.text = "Let's get started"
            else:
                # Show data cards and collapse empty state so it takes 0 height
                self.ids.empty_state.opacity = 0
                self.ids.empty_state.disabled = True
                self.ids.empty_state.height = 0
                self.ids.empty_state.padding = 0
                self.ids.empty_state.spacing = 0
                self.ids.data_panel.opacity = 1
                self.ids.data_panel.disabled = False

                cycle_day = self.viewmodel.get_current_cycle_day()
                prediction = self.viewmodel.get_next_period_prediction()
                ovulation = self.viewmodel.get_ovulation_prediction()

                self.ids.current_cycle_label.text = cycle_day
                self.ids.prediction_label.text = prediction
                self.ids.ovulation_label.text = ovulation

                # Dynamic subtitle
                self.ids.header_subtitle.text = f"Cycle {cycle_day} \u2014 tracking your wellness"

                # Contextual tip
                self.ids.tip_label.text = self._get_tip(cycle_day)
        except Exception:
            pass

    def _get_tip(self, cycle_day: str) -> str:
        try:
            day_num = int(cycle_day.replace("Day ", ""))
        except (ValueError, AttributeError):
            return "Log your symptoms daily for better predictions."

        if day_num <= 5:
            return "During menstruation, stay hydrated and rest when needed."
        elif day_num <= 13:
            return "Follicular phase \u2014 energy levels rise. Great time for new goals!"
        elif day_num <= 16:
            return "Ovulation phase \u2014 you may feel your most energetic and social."
        elif day_num <= 28:
            return "Luteal phase \u2014 prioritise self-care and manage stress levels."
        else:
            return "Your cycle may be longer than average \u2014 keep logging!"

    def load_sample_data(self):
        """Seed sample cycles and daily logs, then refresh the dashboard."""
        self.storage.seed_sample_data()
        self._refresh()

    def go_to_log(self):
        """Switch bottom nav to the Log tab."""
        try:
            nav = self.parent.parent  # MDBottomNavigationItem -> MDBottomNavigation
            nav.switch_tab('screen_log')
        except Exception:
            pass
