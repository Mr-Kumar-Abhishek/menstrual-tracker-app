from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app.models.storage_manager import StorageManager
from datetime import date

KV = '''
<LogEntryView>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"

        MDLabel:
            text: "Log Symptoms"
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

        MDLabel:
            text: "Primary Symptom"
            font_style: "Caption"

        Spinner:
            id: symptoms_field
            text: "None"
            values: ["None", "Cramps", "Headache", "Bloating", "Fatigue", "Acne"]
            size_hint_y: None
            height: "48dp"
            background_color: app.theme_cls.primary_color

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

        MDRaisedButton:
            text: "Save Log"
            pos_hint: {"center_x": .5}
            on_release: root.save_log()

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

    def save_log(self):
        try:
            log_date = date.fromisoformat(self.ids.date_field.text)
            self.storage.add_daily_log(
                log_date=log_date,
                flow_intensity=self.ids.flow_field.text,
                symptoms=self.ids.symptoms_field.text,
                mood=self.ids.mood_field.text
            )
            self.ids.status_label.text = "Saved successfully!"
            self.ids.status_label.theme_text_color = "Custom"
            self.ids.status_label.text_color = [0, 0.7, 0, 1] # Green
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"
            self.ids.status_label.theme_text_color = "Error"
