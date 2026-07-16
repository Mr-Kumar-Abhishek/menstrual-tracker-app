import sqlite3
import os
import logging
from datetime import date

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, db_path="menstrual_tracker.db"):
        self.db_path = db_path
        self._fallback_active = False
        self._fallback_conn = None

    def _resolve_path(self):
        if self.db_path.startswith("file:"):
            return self.db_path
        if os.path.isabs(self.db_path):
            return self.db_path
            
        try:
            from kivy.app import App
            app = App.get_running_app()
            if app and app.user_data_dir:
                return os.path.join(app.user_data_dir, self.db_path)
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

    def _get_connection(self):
        resolved_path = self._resolve_path()
        uri = True if "?mode=memory" in resolved_path else False
        
        try:
            conn = sqlite3.connect(resolved_path, uri=uri)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.OperationalError as e:
            if not self._fallback_active:
                logger.warning(f"Failed to connect to {resolved_path} ({e}). Falling back to in-memory DB.")
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
        cursor.execute("SELECT * FROM cycles WHERE end_date IS NULL ORDER BY start_date DESC LIMIT 1")
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

    def add_daily_log(self, log_date: date, flow_intensity: str = None, symptoms: str = None, mood: str = None, notes: str = None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO daily_logs (date, flow_intensity, symptoms, mood, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (log_date.isoformat(), flow_intensity, symptoms, mood, notes))
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return log_id

    def get_daily_log(self, log_date: date):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_logs WHERE date = ?", (log_date.isoformat(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None

    def get_all_daily_logs(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_logs")
        logs = [dict(row) for row in cursor.fetchall()]
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
