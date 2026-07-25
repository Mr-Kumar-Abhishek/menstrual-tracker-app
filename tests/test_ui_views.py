import os
import pytest
import tempfile
from datetime import date
from kivy.config import Config

# Configure Kivy to not require a window for tests
Config.set('graphics', 'window_state', 'hidden')
Config.set('kivy', 'log_level', 'error')

from main import MenstrualTrackerApp
from app.views.log_view import LogEntryView
from app.views.settings_view import SettingsView
from app.views.dashboard_view import DashboardView
from app.views.calendar_view import CalendarView

from kivy.core.window import Window
Window.size = (800, 600)
from kivy.metrics import Metrics
Metrics.density = 1
Metrics.dpi = 96

@pytest.fixture(scope="session", autouse=True)
def kivy_app():
    # Create the app instance so theme_cls is available for views
    app = MenstrualTrackerApp()
    return app

def test_log_entry_view_ui():
    view = LogEntryView()
    view.storage.initialize_database()
    
    # Check default values in UI
    assert view.ids.flow_field.text == "Medium"
    assert view.ids.symptoms_field.text == "None"
    assert view.ids.mood_field.text == "Neutral"
    assert view.ids.notes_field.text == ""
    
    # Test save log functional logic through UI
    view.ids.notes_field.text = "Test note from UI"
    view.save_log()
    assert "Log saved successfully" in view.ids.status_label.text
    
    # Test start period functional logic
    view.start_period()
    assert "Period started" in view.ids.status_label.text

def test_settings_view_ui():
    view = SettingsView()
    view.storage.initialize_database()
    
    # Viewmodel and UI sync test
    assert view.ids.notif_switch.active is True
    
    # Toggle switch
    view.on_switch_active(view.ids.notif_switch, False)
    assert view.viewmodel.get_notifications_enabled() is False
    assert "Settings saved" in view.ids.status_label.text
    
    # Export data
    view.export_data()
    assert "Data exported to" in view.ids.status_label.text

def test_dashboard_view_ui():
    view = DashboardView()
    view.storage.initialize_database()
    view.on_enter()
    assert view.ids.current_cycle_label.text != ""
    assert view.ids.prediction_label.text != ""

def test_calendar_view_ui():
    view = CalendarView()
    view.storage.initialize_database()
    view.on_enter()
    assert view.ids.month_year_label.text != ""
    # Ensure calendar grid is populated with days
    assert len(view.ids.calendar_grid.children) > 0
