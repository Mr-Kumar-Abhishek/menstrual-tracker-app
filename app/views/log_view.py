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

        MDTextField:
            id: flow_field
            hint_text: "Flow Intensity (Light/Medium/Heavy)"
            mode: "rectangle"

        MDTextField:
            id: symptoms_field
            hint_text: "Symptoms (comma separated)"
            mode: "rectangle"

        MDTextField:
            id: mood_field
            hint_text: "Mood"
            mode: "rectangle"

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
