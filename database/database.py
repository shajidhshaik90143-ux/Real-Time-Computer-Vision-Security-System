import sqlite3
from datetime import datetime


class SecurityDatabase:

    def __init__(self, database_path):

        self.database_path = str(
            database_path
        )

        self.initialize()

    def connect(self):

        return sqlite3.connect(
            self.database_path
        )

    def initialize(self):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                description TEXT,
                severity TEXT,
                timestamp TEXT NOT NULL,
                evidence_path TEXT
            )
            """
        )

        connection.commit()
        connection.close()

    def add_event(
        self,
        event_type,
        description,
        severity="INFO",
        evidence_path=""
    ):

        connection = self.connect()

        cursor = connection.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO events
            (
                event_type,
                description,
                severity,
                timestamp,
                evidence_path
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event_type,
                description,
                severity,
                timestamp,
                evidence_path
            )
        )

        connection.commit()

        event_id = cursor.lastrowid

        connection.close()

        return event_id

    def get_events(self, limit=100):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                event_type,
                description,
                severity,
                timestamp,
                evidence_path
            FROM events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        connection.close()

        return rows

    def count_events(self):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM events"
        )

        count = cursor.fetchone()[0]

        connection.close()

        return count