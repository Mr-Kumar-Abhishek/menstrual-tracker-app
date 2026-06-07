import sqlite3
import os
from datetime import date

class StorageManager:
    def __init__(self, db_path="menstrual_tracker.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_database(self):
        conn = self._get_connection()
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
        
        conn.commit()
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
