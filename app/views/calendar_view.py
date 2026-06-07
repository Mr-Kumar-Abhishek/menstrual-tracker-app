from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

KV = '''
<CalendarView>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            text: "Calendar"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]

        MDCard:
            orientation: "vertical"
            padding: "16dp"
            size_hint: 1, 1
            elevation: 2
            
            MDLabel:
                text: "Calendar Component\\n(Coming Soon: Full Grid View)"
                halign: "center"
                theme_text_color: "Secondary"
'''
Builder.load_string(KV)

class CalendarView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
