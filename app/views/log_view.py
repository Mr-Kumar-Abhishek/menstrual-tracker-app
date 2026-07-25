from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app.models.storage_manager import StorageManager
from app.viewmodels.log_viewmodel import LogViewModel
from datetime import date

KV = '''
<LogEntryView>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"

        MDLabel:
            text: "Log Symptoms & Cycle"
            font_style: "H4"
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

        Spinner:
            id: flow_field
            text: "Medium"
            values: ["Light", "Medium", "Heavy"]
            size_hint_y: None
            height: "48dp"
            background_color: app.theme_cls.primary_color

        MDTextField:
            id: symptoms_field
            hint_text: "Symptoms (e.g. Cramps, Headache)"
            mode: "rectangle"
            text: "None"

        MDLabel:
            text: "Mood"
            font_style: "Caption"

        Spinner:
            id: mood_field
            text: "Neutral"
            values: ["Happy", "Sad", "Irritable", "Anxious", "Neutral", "Mood Swings"]
            size_hint_y: None
            height: "48dp"
            background_color: app.theme_cls.primary_color

        MDTextField:
            id: notes_field
            hint_text: "Personal Notes"
            mode: "rectangle"
            multiline: True
            size_hint_y: None
            height: "80dp"

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "10dp"
            size_hint_y: None
            height: "48dp"
            pos_hint: {"center_x": .5}
            
            MDRaisedButton:
                text: "Save Log"
                on_release: root.save_log()

            MDRaisedButton:
                text: "Start Period"
                md_bg_color: 0.8, 0.2, 0.2, 1
                on_release: root.start_period()
                
            MDRaisedButton:
                text: "End Period"
                md_bg_color: 0.5, 0.5, 0.5, 1
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
