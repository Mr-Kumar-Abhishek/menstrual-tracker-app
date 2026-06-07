from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.clock import Clock
from app.models.storage_manager import StorageManager
from app.viewmodels.calendar_viewmodel import CalendarViewModel
from datetime import date
import calendar

KV = '''
<CalendarView>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "10dp"
        spacing: "10dp"

        # Header
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "48dp"
            
            MDIconButton:
                icon: "chevron-left"
                on_release: root.prev_month()
                
            MDLabel:
                id: month_year_label
                text: "Month Year"
                halign: "center"
                font_style: "H6"
                
            MDIconButton:
                icon: "chevron-right"
                on_release: root.next_month()

        # Legend
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "30dp"
            spacing: "5dp"
            
            # Period Legend
            Widget:
                size_hint_x: None
                width: "20dp"
                canvas:
                    Color:
                        rgba: 0.8, 0.2, 0.2, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
            MDLabel:
                text: "Period"
                font_style: "Caption"

            # Predicted Period
            Widget:
                size_hint_x: None
                width: "20dp"
                canvas:
                    Color:
                        rgba: 0.9, 0.5, 0.5, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
            MDLabel:
                text: "Predicted"
                font_style: "Caption"
                
            # Predicted Ovulation
            Widget:
                size_hint_x: None
                width: "20dp"
                canvas:
                    Color:
                        rgba: 0.2, 0.6, 0.8, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
            MDLabel:
                text: "Ovulation"
                font_style: "Caption"

        # Days of Week Header
        MDGridLayout:
            cols: 7
            size_hint_y: None
            height: "40dp"
            
            MDLabel:
                text: "Mon"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Hint"
            MDLabel:
                text: "Tue"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Hint"
            MDLabel:
                text: "Wed"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Hint"
            MDLabel:
                text: "Thu"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Hint"
            MDLabel:
                text: "Fri"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Hint"
            MDLabel:
                text: "Sat"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Hint"
            MDLabel:
                text: "Sun"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Hint"

        # Calendar Grid
        MDGridLayout:
            id: calendar_grid
            cols: 7
            spacing: "2dp"
            padding: "2dp"
            
'''
Builder.load_string(KV)

class CalendarView(MDScreen):
    current_year = NumericProperty(date.today().year)
    current_month = NumericProperty(date.today().month)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.viewmodel = CalendarViewModel(self.storage)
        Clock.schedule_once(self.populate_calendar, 0.1)
        
    def populate_calendar(self, *args):
        self.ids.calendar_grid.clear_widgets()
        
        month_name = calendar.month_name[self.current_month]
        self.ids.month_year_label.text = f"{month_name} {self.current_year}"
        
        events = self.viewmodel.get_events_for_month(self.current_year, self.current_month)
        
        month_days = calendar.monthcalendar(self.current_year, self.current_month)
        
        for week in month_days:
            for day in week:
                if day == 0:
                    self.ids.calendar_grid.add_widget(MDLabel(text=""))
                else:
                    btn = MDFlatButton(
                        text=str(day),
                        size_hint=(1, 1),
                        font_style="Subtitle1"
                    )
                    
                    # Check for events
                    current_date = date(self.current_year, self.current_month, day)
                    if current_date in events:
                        event_type = events[current_date]['type']
                        if event_type == 'period':
                            btn.md_bg_color = [0.8, 0.2, 0.2, 1] # Red
                            btn.theme_text_color = "Custom"
                            btn.text_color = [1, 1, 1, 1]
                        elif event_type == 'predicted_period':
                            btn.md_bg_color = [0.9, 0.5, 0.5, 1] # Light Pink
                            btn.theme_text_color = "Custom"
                            btn.text_color = [1, 1, 1, 1]
                        elif event_type == 'predicted_ovulation':
                            btn.md_bg_color = [0.2, 0.6, 0.8, 1] # Light Blue
                            btn.theme_text_color = "Custom"
                            btn.text_color = [1, 1, 1, 1]
                    
                    self.ids.calendar_grid.add_widget(btn)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.populate_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.populate_calendar()
        
    def on_enter(self):
        # Refresh when tab is opened
        self.populate_calendar()
