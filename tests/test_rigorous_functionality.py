import os
import json
import sqlite3
import tempfile
import pytest
from datetime import date, timedelta

from kivy.config import Config
Config.set('graphics', 'window_state', 'hidden')
Config.set('kivy', 'log_level', 'error')

from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.metrics import Metrics

from app.models.crypto_manager import CryptoManager
from app.models.storage_manager import StorageManager
from app.models.prediction_engine import PredictionEngine
from app.models.notification_manager import NotificationManager
from app.viewmodels.dashboard_viewmodel import DashboardViewModel
from app.views.dashboard_view import (
    DashboardView,
    strip_widget_elevation_shadow,
    _clean_single_elevation_widget,
)
from app.views.main_view import MainView, InstantTabTransition
from main import MenstrualTrackerApp

Window.size = (800, 600)
Metrics.density = 1
Metrics.dpi = 96


@pytest.fixture(scope="session", autouse=True)
def kivy_app():
    # Initialize MDApp so theme_cls is available for all view instantiations
    app = MenstrualTrackerApp()
    yield app
    # Restore sample data after tests complete
    sm = StorageManager()
    sm.seed_sample_data()


# =============================================================================
# 1. PredictionEngine Robustness & Edge Cases
# =============================================================================

class TestPredictionEngineRigorous:
    def test_null_and_malformed_cycle_entries(self):
        malformed = [
            None,
            {},
            {"start_date": None},
            {"start_date": "not-a-date"},
            {"start_date": "2026/01/01"},  # wrong delimiter
            {"start_date": "2026-01-01", "end_date": "invalid"},
            {"start_date": "2026-01-29", "end_date": "2026-02-02"},
        ]
        engine = PredictionEngine(malformed)
        # Should gracefully ignore invalid entries and only keep valid ones
        assert len(engine.historical_cycles) == 2
        pred = engine.predict_next_period()
        assert pred is not None
        assert pred == date(2026, 1, 29) + timedelta(days=28)

    def test_out_of_order_cycles_sorted_chronologically(self):
        cycles = [
            {"start_date": "2026-03-01", "end_date": "2026-03-05"},
            {"start_date": "2026-01-01", "end_date": "2026-01-05"},
            {"start_date": "2026-02-01", "end_date": "2026-02-05"},
        ]
        engine = PredictionEngine(cycles)
        # Should sort so most recent is 2026-03-01
        assert engine.historical_cycles[-1]["start_date"] == "2026-03-01"
        assert engine.predict_next_period() > date(2026, 3, 1)

    def test_cycle_length_boundaries_and_clamping(self):
        # Extremely long interval (60 days) -> should clamp to 35
        long_cycles = [
            {"start_date": "2026-01-01", "end_date": "2026-01-05"},
            {"start_date": "2026-03-02", "end_date": "2026-03-06"},
        ]
        engine_long = PredictionEngine(long_cycles)
        assert (engine_long.predict_next_period() - date(2026, 3, 2)).days == 35

        # Extremely short interval (12 days) -> should clamp to 21
        short_cycles = [
            {"start_date": "2026-01-01", "end_date": "2026-01-05"},
            {"start_date": "2026-01-13", "end_date": "2026-01-17"},
        ]
        engine_short = PredictionEngine(short_cycles)
        assert (engine_short.predict_next_period() - date(2026, 1, 13)).days == 21

    def test_period_duration_clamping(self):
        # Duration over 10 days -> clamp to 10
        extreme_duration = [
            {"start_date": "2026-01-01", "end_date": "2026-01-20"}
        ]
        engine = PredictionEngine(extreme_duration)
        next_start = engine.predict_next_period()
        next_end = engine.predict_next_period_end_date()
        assert (next_end - next_start).days + 1 == 10

        # Duration under 2 days -> clamp to 2
        short_duration = [
            {"start_date": "2026-01-01", "end_date": "2026-01-01"}
        ]
        engine_short = PredictionEngine(short_duration)
        next_s = engine_short.predict_next_period()
        next_e = engine_short.predict_next_period_end_date()
        assert (next_e - next_s).days + 1 == 2

    def test_ovulation_window_calculation(self):
        cycles = [{"start_date": "2026-05-01", "end_date": "2026-05-05"}]
        engine = PredictionEngine(cycles)
        start_ov, end_ov = engine.predict_ovulation_window()
        # Next period is 2026-05-29, ovulation is day 14 before (2026-05-15)
        # Window is +/- 2 days: 2026-05-13 to 2026-05-17
        assert start_ov == date(2026, 5, 13)
        assert end_ov == date(2026, 5, 17)
        assert (end_ov - start_ov).days == 4


# =============================================================================
# 2. CryptoManager Security & Resiliency
# =============================================================================

class TestCryptoManagerRigorous:
    def test_aes_gcm_roundtrip_various_payloads(self, tmp_path):
        key_file = str(tmp_path / "secret.key")
        cm = CryptoManager(key_file)

        test_payloads = [
            "Normal text",
            "Unicode and emojis: 🩸💊🌸 サイクル 💖",
            "SQL characters: '; DROP TABLE cycles; --",
            "Long text: " + ("A" * 5000),
            "",
            "Newline\nand\ttabs\r\n",
        ]

        for payload in test_payloads:
            encrypted = cm.encrypt(payload)
            assert encrypted.startswith("AES256GCM$")
            decrypted = cm.decrypt(encrypted)
            assert decrypted == payload

    def test_null_payload_handling(self, tmp_path):
        cm = CryptoManager(str(tmp_path / "secret.key"))
        assert cm.encrypt(None) is None
        assert cm.decrypt(None) is None

    def test_tampered_ciphertext_fails_gracefully(self, tmp_path):
        cm = CryptoManager(str(tmp_path / "secret.key"))
        ciphertext = cm.encrypt("Sensitive Health Data")
        # Tamper with the base64 payload
        tampered = ciphertext[:-4] + "AAAA"
        # Should return raw data on authentication failure rather than raising
        res = cm.decrypt(tampered)
        assert res == tampered

    def test_legacy_key_length_recovery(self, tmp_path):
        key_file = str(tmp_path / "secret.key")
        # Write an invalid length key (e.g. 44 bytes Fernet key)
        with open(key_file, "wb") as f:
            f.write(b"a" * 44)

        cm = CryptoManager(key_file)
        assert len(cm.key) == 32
        with open(key_file, "rb") as f:
            assert len(f.read()) == 32


# =============================================================================
# 3. StorageManager Database Integrity & Plaintext Migration
# =============================================================================

class TestStorageManagerRigorous:
    def test_sqlite_fallback_on_corrupt_file(self, tmp_path):
        corrupt_db = str(tmp_path / "corrupt.db")
        with open(corrupt_db, "wb") as f:
            f.write(b"NOT A SQLITE FILE HEADER")

        sm = StorageManager(corrupt_db, str(tmp_path / "secret.key"))
        sm.initialize_database()
        assert sm._fallback_active is True
        # Ensure CRUD operations work even in fallback mode
        cid = sm.add_cycle(date.today())
        assert cid is not None
        assert len(sm.get_all_cycles()) == 1

    def test_legacy_plaintext_migration_to_aes256gcm(self, tmp_path):
        db_path = str(tmp_path / "unencrypted.db")
        conn = sqlite3.connect(db_path)
        conn.execute('''CREATE TABLE daily_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE NOT NULL,
            flow_intensity TEXT,
            symptoms TEXT,
            mood TEXT,
            notes TEXT
        )''')
        conn.execute('''INSERT INTO daily_logs VALUES (1, '2026-01-01', 'Heavy', 'Cramps', 'Sad', 'Plaintext note')''')
        conn.commit()
        conn.close()

        sm = StorageManager(db_path, str(tmp_path / "secret.key"))
        sm.initialize_database()

        # Check raw database rows: they must be encrypted
        raw_conn = sqlite3.connect(db_path)
        cur = raw_conn.cursor()
        cur.execute("SELECT flow_intensity, symptoms, mood, notes FROM daily_logs WHERE log_id=1")
        row = cur.fetchone()
        raw_conn.close()

        for val in row:
            assert val.startswith("AES256GCM$")

        # Decrypted retrieval via API
        log = sm.get_daily_log(date(2026, 1, 1))
        assert log["flow_intensity"] == "Heavy"
        assert log["symptoms"] == "Cramps"
        assert log["notes"] == "Plaintext note"

    def test_seed_sample_data_creates_valid_cycle_timeline(self, tmp_path):
        sm = StorageManager(str(tmp_path / "test.db"), str(tmp_path / "secret.key"))
        sm.seed_sample_data()

        cycles = sm.get_all_cycles()
        assert len(cycles) == 3
        # Ensure chronological descending order
        assert date.fromisoformat(cycles[0]["start_date"]) > date.fromisoformat(cycles[1]["start_date"])
        assert date.fromisoformat(cycles[1]["start_date"]) > date.fromisoformat(cycles[2]["start_date"])

        logs = sm.get_all_daily_logs()
        assert len(logs) == 4
        assert any(l["mood"] == "Happy" for l in logs)


# =============================================================================
# 4. NotificationManager Resilience
# =============================================================================

class TestNotificationManagerRigorous:
    def test_notification_catches_platform_exceptions(self, monkeypatch):
        nm = NotificationManager()
        def mock_failing_notify(**kwargs):
            raise RuntimeError("Android Notification Permission Denied")

        import plyer
        monkeypatch.setattr(plyer.notification, "notify", mock_failing_notify)
        # Should not raise exception
        nm._send_notification("Test Title", "Test Message")


# =============================================================================
# 5. DashboardView & MainView UI Shadow & WeakMethod Integrity
# =============================================================================

class TestUIElevationAndScrollRigorous:
    def test_weakmethod_safe_kivymd_elevation_callbacks(self):
        from kivymd.uix.behaviors import CommonElevationBehavior
        from kivy.weakmethod import WeakMethod

        # 1. Verify the exact WeakMethod mechanics that prevented crashes:
        # Kivy's EventDispatcher / Clock weakmethod uses fn.__name__ to lookup getattr(proxy, method_name).
        class TargetClass:
            def on_pos(self):
                return "pos_called"

        target = TargetClass()
        wm_valid = WeakMethod(target.on_pos)
        assert wm_valid.method_name == "on_pos"
        assert wm_valid()() == "pos_called"

        # Simulating the bug where a generic '_noop_elevation_method' was bound:
        def _noop_elevation_method(self):
            return "noop"

        target.on_size = _noop_elevation_method.__get__(target, TargetClass)
        wm_invalid = WeakMethod(target.on_size)
        assert wm_invalid.method_name == "_noop_elevation_method"
        # wm_invalid() executes getattr(target, "_noop_elevation_method") which fails with AttributeError:
        with pytest.raises(AttributeError):
            wm_invalid()

        # 2. Check if CommonElevationBehavior in current KivyMD has shader hooks (KivyMD 1.1.x)
        if hasattr(CommonElevationBehavior, "set_shader_string"):
            for method_name in ("on_pos", "on_size", "set_shader_string", "on_elevation", "on_shadow_color", "hide_elevation"):
                fn = getattr(CommonElevationBehavior, method_name)
                assert fn.__name__ == method_name, f"Expected fn.__name__ == {method_name}, got {fn.__name__}"
                # WeakMethod on the class function when bound to an instance will resolve cleanly
                target_w = CommonElevationBehavior()
                bound_fn = getattr(target_w, method_name)
                wm = WeakMethod(bound_fn)
                assert wm.method_name == method_name
                # Calling wm() must resolve without AttributeError
                res = wm()
                assert res is not None

    def test_dashboard_cards_have_zero_elevation_and_shadow(self):
        dv = DashboardView()
        cards = [w for w in dv.walk() if w.__class__.__name__ == "MDCard"]
        assert len(cards) == 4
        for card in cards:
            assert card.elevation == 0
            assert list(card.shadow_color) == [0.0, 0.0, 0.0, 0.0]

    def test_scrollview_configuration_for_no_scroll_shadow(self):
        dv = DashboardView()
        sp = dv.ids.data_panel
        assert isinstance(sp.effect_cls(), ScrollEffect)
        assert sp.always_overscroll is False
        assert sp.bar_color[3] <= 0.3
        assert list(sp.bar_inactive_color) == [0.0, 0.0, 0.0, 0.0]

    def test_clean_single_elevation_widget(self):
        from kivymd.uix.card import MDCard
        card = MDCard()
        card._elevation = 12
        card._shadow_color = [0.0, 0.0, 0.0, 0.5]
        _clean_single_elevation_widget(card)
        assert card._elevation == 0
        assert list(card._shadow_color) == [0.0, 0.0, 0.0, 0.0]

    def test_strip_widget_elevation_shadow_tree(self):
        dv = DashboardView()
        strip_widget_elevation_shadow(dv)
        for w in dv.walk():
            if hasattr(w, "elevation"):
                assert w.elevation == 0
            if hasattr(w, "_elevation"):
                assert w._elevation == 0

    def test_main_view_tab_transitions_and_safe_insets(self):
        mv = MainView()
        assert mv.bottom_safe_inset > 0
        assert mv.ids.bottom_nav.transition is InstantTabTransition
        # Test tab switching across all 4 screens
        for screen_name in ("screen_calendar", "screen_log", "screen_settings", "screen_dashboard"):
            mv.ids.bottom_nav.switch_tab(screen_name)
            assert mv.ids.bottom_nav.ids.tab_manager.current == screen_name
