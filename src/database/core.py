import sqlite3

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
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

    def edit_session(self, session_id, activity=None, duration=None, date=None, notes=None):
            fields = []
            values = []

            if activity is not None:
                fields.append("activity = ?")
                values.append(activity)

            if duration is not None:
                fields.append("duration_minutes = ?")
                values.append(duration)

            if date is not None:
                fields.append("session_date = ?")
                values.append(date)

            if notes is not None:
                fields.append("notes = ?")
                values.append(notes)

            if not fields:
                return False

            values.append(session_id)

            query = f"""
                UPDATE sessions
                SET {", ".join(fields)}
                WHERE session_id = ?
            """

            self.cur.execute(query, tuple(values))
            self.conn.commit()
    
    def read_session(self, session_id=None):

        if session_id is not None:
            res = self.cur.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        else:
            res = self.cur.execute("SELECT * FROM sessions")
          
        return [dict(row) for row in res.fetchall()]
    
    def close(self):
        self.conn.close()

