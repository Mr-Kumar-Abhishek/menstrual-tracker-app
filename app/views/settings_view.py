from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from app.models.storage_manager import StorageManager
from app.viewmodels.settings_viewmodel import SettingsViewModel
import os

KV = '''
<SettingsView>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            text: "Settings"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "48dp"
            
            MDLabel:
                text: "Enable Notifications"
                valign: "center"

            MDSwitch:
                id: notif_switch
                active: True
                on_active: root.on_switch_active(*args)
                pos_hint: {'center_y': .5}

        MDRaisedButton:
            text: "Export Data to JSON"
            pos_hint: {"center_x": .5}
            on_release: root.export_data()

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


class SettingsView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.viewmodel = SettingsViewModel(self.storage)

    def on_enter(self, *args):
        self.ids.notif_switch.active = self.viewmodel.get_notifications_enabled()

    def on_switch_active(self, switch, value):
        self.viewmodel.set_notifications_enabled(value)
        self.ids.status_label.text = "Settings saved."
        self.ids.status_label.theme_text_color = "Custom"
        self.ids.status_label.text_color = [0, 0.7, 0, 1]

    def export_data(self):
        try:
            # For simplicity, we save it in the current working directory.
            # On Android, it would be better to use android platform APIs.
            export_path = os.path.join(
                os.getcwd(), 'menstrual_tracker_export.json')
            self.viewmodel.export_data(export_path)
            self.ids.status_label.text = f"Data exported to:\n{export_path}"
            self.ids.status_label.theme_text_color = "Custom"
            self.ids.status_label.text_color = [0, 0.7, 0, 1]
        except Exception as e:
            self.ids.status_label.text = f"Export failed: {str(e)}"
            self.ids.status_label.theme_text_color = "Error"
