import sqlite3
import os
import shutil
import logging
from datetime import date, timedelta
from app.models.crypto_manager import CryptoManager

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, db_path="menstrual_tracker.db", key_path="secret.key"):
        self.db_path = db_path
        self.key_path = key_path
        self._fallback_active = False
        self._fallback_conn = None
        self.crypto = CryptoManager(key_path)

    def _resolve_path(self):
        if self.db_path.startswith("file:"):
            return self.db_path
        if os.path.isabs(self.db_path):
            return self.db_path

        try:
            from kivy.app import App
            app = App.get_running_app()
            if app and app.user_data_dir:
                os.makedirs(app.user_data_dir, exist_ok=True)
                target_path = os.path.join(app.user_data_dir, self.db_path)
                if not os.path.exists(target_path):
                    base_dir = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), "..", "..")
                    )
                    bundled_db = os.path.join(base_dir, os.path.basename(self.db_path))
                    bundled_key = os.path.join(base_dir, os.path.basename(self.key_path))
                    if os.path.exists(bundled_db):
                        if os.path.exists(bundled_key) and os.path.getsize(bundled_key) == 32:
                            target_key = os.path.join(
                                app.user_data_dir, os.path.basename(self.key_path)
                            )
                            shutil.copy2(bundled_key, target_key)
                            self.crypto = CryptoManager(self.key_path)
                        shutil.copy2(bundled_db, target_path)
                return target_path
        except Exception:
            pass

        return self.db_path

    def _create_tables(self, conn):
        cursor = conn.cursor()

        # Create cycles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cycles (
                cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_date DATE NOT NULL,
                end_date DATE,
                cycle_length INTEGER
            )
        ''')

        # Create daily_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE NOT NULL,
                flow_intensity TEXT,
                symptoms TEXT,
                mood TEXT,
                notes TEXT
            )
        ''')

        # Create settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        conn.commit()

    def _ensure_encrypted_logs(self, conn):
        """Ensure any legacy plaintext rows in daily_logs are encrypted with AES-256-GCM."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT log_id, flow_intensity, symptoms, mood, notes FROM daily_logs"
        )
        rows = cursor.fetchall()
        updated = False
        for row in rows:
            fields = ("flow_intensity", "symptoms", "mood", "notes")
            needs_enc = any(
                row[f] is not None and not str(row[f]).startswith("AES256GCM$")
                for f in fields
            )
            if needs_enc:
                enc_vals = [
                    self.crypto.encrypt(row[f])
                    if (row[f] is not None and not str(row[f]).startswith("AES256GCM$"))
                    else row[f]
                    for f in fields
                ]
                cursor.execute(
                    '''
                    UPDATE daily_logs
                    SET flow_intensity = ?, symptoms = ?, mood = ?, notes = ?
                    WHERE log_id = ?
                    ''',
                    (*enc_vals, row["log_id"]),
                )
                updated = True
        if updated:
            conn.commit()

    def _get_connection(self):
        resolved_path = self._resolve_path()
        uri = True if "?mode=memory" in resolved_path else False

        try:
            conn = sqlite3.connect(resolved_path, uri=uri)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.OperationalError as e:
            if not self._fallback_active:
                logger.warning(
                    f"Failed to connect to {resolved_path} ({e}). Falling back to in-memory DB.")
                self.db_path = "file:memdb1?mode=memory&cache=shared"
                self._fallback_active = True
                # Keep a persistent connection to prevent the shared memory DB from being destroyed
                self._fallback_conn = sqlite3.connect(self.db_path, uri=True)
                self._create_tables(self._fallback_conn)

            conn = sqlite3.connect(self.db_path, uri=True)
            conn.row_factory = sqlite3.Row
            return conn

    def initialize_database(self):
        conn = self._get_connection()
        self._create_tables(conn)
        self._ensure_encrypted_logs(conn)
        conn.close()

    def add_cycle(self, start_date: date, end_date: date = None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cycles (start_date, end_date)
            VALUES (?, ?)
        ''', (start_date.isoformat(), end_date.isoformat() if end_date else None))

        cycle_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cycle_id

    def get_all_cycles(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cycles ORDER BY start_date DESC")
        cycles = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return cycles

    def get_active_cycle(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM cycles WHERE end_date IS NULL ORDER BY start_date DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None

    def update_cycle_end_date(self, cycle_id: int, end_date: date):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE cycles SET end_date = ? WHERE cycle_id = ?
        ''', (end_date.isoformat(), cycle_id))
        conn.commit()
        conn.close()

    def _decrypt_log_row(self, row):
        if not row:
            return None
        d_row = dict(row)
        d_row['flow_intensity'] = self.crypto.decrypt(
            d_row.get('flow_intensity')) if d_row.get('flow_intensity') else None
        d_row['symptoms'] = self.crypto.decrypt(
            d_row.get('symptoms')) if d_row.get('symptoms') else None
        d_row['mood'] = self.crypto.decrypt(
            d_row.get('mood')) if d_row.get('mood') else None
        d_row['notes'] = self.crypto.decrypt(
            d_row.get('notes')) if d_row.get('notes') else None
        return d_row

    def add_daily_log(self, log_date: date, flow_intensity: str = None, symptoms: str = None, mood: str = None, notes: str = None):
        enc_flow = self.crypto.encrypt(
            flow_intensity) if flow_intensity else None
        enc_symptoms = self.crypto.encrypt(symptoms) if symptoms else None
        enc_mood = self.crypto.encrypt(mood) if mood else None
        enc_notes = self.crypto.encrypt(notes) if notes else None

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO daily_logs (date, flow_intensity, symptoms, mood, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (log_date.isoformat(), enc_flow, enc_symptoms, enc_mood, enc_notes))

        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return log_id

    def get_daily_log(self, log_date: date):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_logs WHERE date = ?",
                       (log_date.isoformat(),))
        row = cursor.fetchone()
        conn.close()
        return self._decrypt_log_row(row)

    def get_all_daily_logs(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_logs")
        logs = [self._decrypt_log_row(row) for row in cursor.fetchall()]
        conn.close()
        return logs

    def get_setting(self, key: str, default_value: str = None) -> str:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row['value']
        return default_value

    def set_setting(self, key: str, value: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, value))
        conn.commit()
        conn.close()

    def seed_sample_data(self):
        """Populate the database with 3 realistic 28-day cycles and encrypted daily logs."""
        self.initialize_database()
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cycles")
        cursor.execute("DELETE FROM daily_logs")
        conn.commit()
        conn.close()

        today = date.today()
        c3_start = today - timedelta(days=9)   # Day 10 of current cycle
        c2_start = c3_start - timedelta(days=28)
        c1_start = c2_start - timedelta(days=28)

        self.add_cycle(c1_start, c1_start + timedelta(days=4))
        self.add_cycle(c2_start, c2_start + timedelta(days=4))
        self.add_cycle(c3_start, c3_start + timedelta(days=4))

        self.add_daily_log(
            c3_start,
            flow_intensity="Heavy",
            symptoms="Cramps, Fatigue",
            mood="Irritable",
            notes="First day of period, rested in the afternoon.",
        )
        self.add_daily_log(
            c3_start + timedelta(days=2),
            flow_intensity="Medium",
            symptoms="Mild headache",
            mood="Sad",
            notes="Staying hydrated and drinking herbal tea.",
        )
        self.add_daily_log(
            c3_start + timedelta(days=4),
            flow_intensity="Light",
            symptoms="None",
            mood="Neutral",
            notes="Period wrapping up, energy returning.",
        )
        self.add_daily_log(
            today,
            flow_intensity="Light",
            symptoms="None",
            mood="Happy",
            notes="Feeling energetic today!",
        )

    def export_data(self, file_path: str):
        import json
        cycles = self.get_all_cycles()
        logs = self.get_all_daily_logs()

        data = {
            "cycles": cycles,
            "daily_logs": logs
        }

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
