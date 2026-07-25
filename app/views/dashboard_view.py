from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app.viewmodels.dashboard_viewmodel import DashboardViewModel
from app.models.storage_manager import StorageManager

KV = '''
<DashboardView>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            text: "Dashboard"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]

        MDCard:
            orientation: "vertical"
            padding: "16dp"
            size_hint: 1, None
            height: "120dp"
            elevation: 2

            MDLabel:
                text: "Current Cycle"
                theme_text_color: "Secondary"

            MDLabel:
                id: current_cycle_label
                text: "Loading..."
                font_style: "H5"

        MDCard:
            orientation: "vertical"
            padding: "16dp"
            size_hint: 1, None
            height: "120dp"
            elevation: 2

            MDLabel:
                text: "Next Period Prediction"
                theme_text_color: "Secondary"

            MDLabel:
                id: prediction_label
                text: "Loading..."
                font_style: "H5"

        MDCard:
            orientation: "vertical"
            padding: "16dp"
            size_hint: 1, None
            height: "120dp"
            elevation: 2

            MDLabel:
                text: "Ovulation Window"
                theme_text_color: "Secondary"

            MDLabel:
                id: ovulation_label
                text: "Loading..."
                font_style: "H5"

        Widget:
'''
Builder.load_string(KV)


class DashboardView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # In a real app, storage is passed down or accessed via dependency injection
        self.storage = StorageManager()
        self.storage.initialize_database()
        self.viewmodel = DashboardViewModel(self.storage)

    def on_enter(self, *args):
        self.ids.current_cycle_label.text = self.viewmodel.get_current_cycle_day()
        self.ids.prediction_label.text = self.viewmodel.get_next_period_prediction()
        self.ids.ovulation_label.text = self.viewmodel.get_ovulation_prediction()
