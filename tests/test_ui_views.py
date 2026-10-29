import os
import sqlite3
import tempfile
from kivy.metrics import Metrics
from kivy.core.window import Window
from kivymd.uix.label import MDIcon
from app.models.storage_manager import StorageManager
from app.viewmodels.dashboard_viewmodel import DashboardViewModel
from app.views.calendar_view import CalendarView
from app.views.dashboard_view import DashboardView
from app.views.settings_view import SettingsView
from app.views.log_view import LogEntryView
from app.views.main_view import MainView, InstantTabTransition
from main import MenstrualTrackerApp
import pytest
from kivy.config import Config

# Configure Kivy to not require a window for tests
Config.set('graphics', 'window_state', 'hidden')
Config.set('kivy', 'log_level', 'error')


Window.size = (800, 600)
Metrics.density = 1
Metrics.dpi = 96


@pytest.fixture(scope="session", autouse=True)
def kivy_app():
    # Create the app instance so theme_cls is available for views
    app = MenstrualTrackerApp()
    yield app
    # Restore clean encrypted sample data in default DB and export file after UI tests
    sm = StorageManager()
    sm.seed_sample_data()
    sm.set_setting("notifications_enabled", "True")
    sm.export_data("menstrual_tracker_export.json")


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
    view.storage.set_setting("notifications_enabled", "True")
    view.ids.notif_switch.active = True

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


def test_load_sample_data_ui():
    fd, tmp_db = tempfile.mkstemp()
    os.close(fd)
    try:
        view = DashboardView()
        view.storage = StorageManager(tmp_db)
        view.storage.initialize_database()
        view.viewmodel = DashboardViewModel(view.storage)
        view.on_enter()
        assert view.ids.empty_state.opacity == 1

        view.load_sample_data()
        assert view.ids.empty_state.opacity == 0
        assert view.ids.data_panel.opacity == 1
        assert view.ids.current_cycle_label.text == "Day 10"
        assert len(view.storage.get_all_cycles()) == 3
        assert len(view.storage.get_all_daily_logs()) == 4

        # Verify raw SQLite rows are encrypted with AES256GCM$
        conn = sqlite3.connect(tmp_db)
        cur = conn.cursor()
        cur.execute("SELECT flow_intensity, symptoms, mood, notes FROM daily_logs")
        rows = cur.fetchall()
        conn.close()
        assert len(rows) == 4
        for row in rows:
            for col in row:
                assert col.startswith("AES256GCM$")
    finally:
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


def test_app_and_dashboard_icons():
    app = MenstrualTrackerApp()
    app.build()
    assert os.path.exists(app.icon)
    assert app.icon.endswith(("icon.png", "icon.jpg"))

    view = DashboardView()
    icon_names = [w.icon for w in view.walk() if isinstance(w, MDIcon)]
    for expected in ("calendar-heart", "calendar-today", "water", "star-circle", "lightbulb-on-outline"):
        assert expected in icon_names


def test_calendar_view_ui():
    view = CalendarView()
    view.storage.initialize_database()
    view.on_enter()
    assert view.ids.month_year_label.text != ""
    # Ensure calendar grid is populated with days
    assert len(view.ids.calendar_grid.children) > 0
    # Ensure day buttons do not enforce KivyMD's 64dp minimum width (prevents 7-col overflow on mobile)
    day_buttons = [w for w in view.ids.calendar_grid.children if hasattr(w, "_min_width")]
    assert len(day_buttons) > 0
    assert all(btn._min_width == 0 for btn in day_buttons)


def test_main_view_rendering_and_tab_transitions():
    mv = MainView()
    assert mv.ids.bottom_nav.transition is InstantTabTransition
    assert isinstance(mv.ids.bottom_nav.ids.tab_manager.transition, InstantTabTransition)
    assert mv.bottom_safe_inset > 0
    assert mv.ids.bottom_nav.padding[3] == mv.bottom_safe_inset
    assert mv.ids.dashboard_view.ids.current_cycle_label.text != ""
    for tab_name in ("screen_calendar", "screen_log", "screen_settings", "screen_dashboard"):
        mv.ids.bottom_nav.switch_tab(tab_name)
        assert mv.ids.bottom_nav.ids.tab_manager.current == tab_name
        assert isinstance(mv.ids.bottom_nav.ids.tab_manager.transition, InstantTabTransition)

    # Verify Android Back button (key 27) navigates back to Dashboard from other tabs
    mv.ids.bottom_nav.switch_tab("screen_settings")
    assert mv.ids.bottom_nav.ids.tab_manager.current == "screen_settings"
    assert mv._on_keyboard(None, 27) is True
    assert mv.ids.bottom_nav.ids.tab_manager.current == "screen_dashboard"
    assert mv._on_keyboard(None, 27) is False

