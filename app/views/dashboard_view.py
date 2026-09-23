from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app.viewmodels.dashboard_viewmodel import DashboardViewModel
from app.models.storage_manager import StorageManager

KV = '''
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
            spacing: "16dp"
            size_hint_y: None
            height: "360dp"
            opacity: 0

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
                text: "  Log First Period  "
                icon: "plus-circle"
                pos_hint: {"center_x": 0.5}
                md_bg_color: app.theme_cls.primary_color
                on_release: root.go_to_log()

        # ── Data cards (shown when data exists) ─────────────────
        ScrollView:
            id: data_panel
            opacity: 0

            MDBoxLayout:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "12dp"
                adaptive_height: True

                # Current Cycle card
                MDCard:
                    orientation: "horizontal"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint: 1, None
                    height: "90dp"
                    elevation: 1
                    radius: [12,]

                    MDIcon:
                        icon: "calendar-today"
                        font_size: "36sp"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        size_hint_x: None
                        width: "48dp"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "4dp"

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
                    elevation: 1
                    radius: [12,]

                    MDIcon:
                        icon: "water"
                        font_size: "36sp"
                        theme_text_color: "Custom"
                        text_color: 0.85, 0.15, 0.45, 1
                        size_hint_x: None
                        width: "48dp"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "4dp"

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
                    elevation: 1
                    radius: [12,]

                    MDIcon:
                        icon: "star-circle"
                        font_size: "36sp"
                        theme_text_color: "Custom"
                        text_color: 0.98, 0.6, 0.1, 1
                        size_hint_x: None
                        width: "48dp"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "4dp"

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
                    md_bg_color: app.theme_cls.primary_light[:3] + [0.12]
                    radius: [12,]

                    MDIcon:
                        icon: "lightbulb-on-outline"
                        font_size: "28sp"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        size_hint_x: None
                        width: "40dp"

                    MDLabel:
                        id: tip_label
                        text: ""
                        font_style: "Caption"
                        theme_text_color: "Secondary"
                        text_size: self.width, None

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

    def on_enter(self, *args):
        self._refresh()

    def _refresh(self):
        cycles = self.storage.get_all_cycles()
        has_data = bool(cycles)

        if not has_data:
            # Show empty / onboarding state
            self.ids.empty_state.opacity = 1
            self.ids.data_panel.opacity = 0
            self.ids.header_subtitle.text = "Let's get started \U0001f331"
        else:
            # Show data cards
            self.ids.empty_state.opacity = 0
            self.ids.data_panel.opacity = 1

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

    def _get_tip(self, cycle_day: str) -> str:
        try:
            day_num = int(cycle_day.replace("Day ", ""))
        except (ValueError, AttributeError):
            return "\U0001f4a7 Log your symptoms daily for better predictions."

        if day_num <= 5:
            return "\U0001f4a7 During menstruation, stay hydrated and rest when needed."
        elif day_num <= 13:
            return "\u2b50 Follicular phase — energy levels rise. Great time for new goals!"
        elif day_num <= 16:
            return "\U0001f31f Ovulation phase — you may feel your most energetic and social."
        elif day_num <= 28:
            return "\U0001f319 Luteal phase — prioritise self-care and manage stress levels."
        else:
            return "\U0001f4c5 Your cycle may be longer than average — keep logging!"

    def go_to_log(self):
        """Switch bottom nav to the Log tab."""
        try:
            nav = self.parent.parent  # MDBottomNavigationItem -> MDBottomNavigation
            nav.switch_tab('screen_log')
        except Exception:
            pass
