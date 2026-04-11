import sqlite3

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self._create_database()

    def _create_database(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS sessions (
                         session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                         activity TEXT NOT NULL,
                         duration_minutes INT NOT NULL,
                         session_date TEXT NOT NULL,
                         notes TEXT
                         )""")
        self.conn.commit()

    def add_session(self, activity, duration, date, notes=""):
        self.cur.execute("""INSERT INTO sessions (activity, duration_minutes, session_date, notes)
                         VALUES (?, ?, ?, ?)""", (activity, duration, date, notes))
        

        self.conn.commit()

    def delete_session(self, session_id):
        self.cur.execute("""DELETE FROM sessions
                            WHERE session_id = ?;""", (session_id,))

        self.conn.commit()