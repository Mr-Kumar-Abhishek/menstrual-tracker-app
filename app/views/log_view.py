from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app.models.storage_manager import StorageManager
from app.viewmodels.log_viewmodel import LogViewModel
from datetime import date

KV = '''
<LogEntryView>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "16dp", "14dp", "16dp", "16dp"
        spacing: "10dp"
        md_bg_color: app.theme_cls.bg_normal

        MDLabel:
            text: "Log Symptoms & Cycle"
            font_style: "H5"
            bold: True
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]

        MDTextField:
            id: date_field
            hint_text: "Date (YYYY-MM-DD)"
            text: root.today_str
            mode: "rectangle"

        MDLabel:
            text: "Flow Intensity"
            font_style: "Caption"
            size_hint_y: None
            height: self.texture_size[1]

        Spinner:
            id: flow_field
            text: "Medium"
            values: ["Light", "Medium", "Heavy"]
            size_hint_y: None
            height: "40dp"
            background_normal: ""
            background_down: ""
            background_color: app.theme_cls.primary_color
            color: 1, 1, 1, 1
            bold: True

        MDTextField:
            id: symptoms_field
            hint_text: "Symptoms (e.g. Cramps, Headache)"
            mode: "rectangle"
            text: "None"

        MDLabel:
            text: "Mood"
            font_style: "Caption"
            size_hint_y: None
            height: self.texture_size[1]

        Spinner:
            id: mood_field
            text: "Neutral"
            values: ["Happy", "Sad", "Irritable", "Anxious", "Neutral", "Mood Swings"]
            size_hint_y: None
            height: "40dp"
            background_normal: ""
            background_down: ""
            background_color: app.theme_cls.primary_color
            color: 1, 1, 1, 1
            bold: True

        MDTextField:
            id: notes_field
            hint_text: "Personal Notes"
            mode: "rectangle"
            multiline: True
            size_hint_y: None
            height: "60dp"

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "8dp"
            size_hint_x: 1
            size_hint_y: None
            height: "44dp"

            MDRaisedButton:
                text: "Save Log"
                size_hint_x: 1
                _min_width: 0
                padding: "4dp", "10dp"
                elevation: 0
                shadow_color: 0, 0, 0, 0
                on_release: root.save_log()

            MDRaisedButton:
                text: "Start Period"
                size_hint_x: 1
                _min_width: 0
                padding: "4dp", "10dp"
                elevation: 0
                shadow_color: 0, 0, 0, 0
                md_bg_color: 0.85, 0.22, 0.27, 1
                on_release: root.start_period()

            MDRaisedButton:
                text: "End Period"
                size_hint_x: 1
                _min_width: 0
                padding: "4dp", "10dp"
                elevation: 0
                shadow_color: 0, 0, 0, 0
                md_bg_color: 0.42, 0.45, 0.49, 1
                on_release: root.end_period()

        MDLabel:
            id: status_label
            text: ""
            theme_text_color: "Hint"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]

        Widget:
'''
Builder.load_string(KV)


class LogEntryView(MDScreen):
    def __init__(self, **kwargs):
        self.today_str = date.today().isoformat()
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.viewmodel = LogViewModel(self.storage)

    def save_log(self):
        try:
            log_date = date.fromisoformat(self.ids.date_field.text)
            self.viewmodel.save_daily_log(
                log_date=log_date,
                flow=self.ids.flow_field.text,
                symptoms=self.ids.symptoms_field.text,
                mood=self.ids.mood_field.text,
                notes=self.ids.notes_field.text
            )
            self.ids.status_label.text = "Log saved successfully!"
            self.ids.status_label.theme_text_color = "Custom"
            self.ids.status_label.text_color = [0, 0.7, 0, 1]  # Green
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"
            self.ids.status_label.theme_text_color = "Error"

    def start_period(self):
        try:
            log_date = date.fromisoformat(self.ids.date_field.text)
            self.viewmodel.start_period(start_date=log_date)
            self.ids.status_label.text = "Period started!"
            self.ids.status_label.theme_text_color = "Custom"
            self.ids.status_label.text_color = [0, 0.7, 0, 1]
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"
            self.ids.status_label.theme_text_color = "Error"

    def end_period(self):
        try:
            log_date = date.fromisoformat(self.ids.date_field.text)
            if not self.viewmodel.is_period_active():
                self.ids.status_label.text = "No active period to end."
                self.ids.status_label.theme_text_color = "Error"
                return
            self.viewmodel.end_period(end_date=log_date)
            self.ids.status_label.text = "Period ended!"
            self.ids.status_label.theme_text_color = "Custom"
            self.ids.status_label.text_color = [0, 0.7, 0, 1]
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"
            self.ids.status_label.theme_text_color = "Error"
