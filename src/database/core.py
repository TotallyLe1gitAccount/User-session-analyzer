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

    def add_session(self, activity : str, duration : int, date : str, notes : str=""):

        if not isinstance(activity, str):
            raise TypeError("activity must be str")
        if not isinstance(duration, int):
            raise TypeError("duration must be int")
        if not isinstance(date, str):
            raise TypeError("date must be str")
        if not isinstance(notes, str):
            raise TypeError("notes must be str")
        
        self.cur.execute("""INSERT INTO sessions (activity, duration_minutes, session_date, notes)
                            VALUES (?, ?, ?, ?)""", (activity, duration, date, notes))
            
        self.conn.commit()
        return self.cur.lastrowid
        
        except sqlite3.Error as e:
            print(f"DB error: {e}")
            return None

    def delete_session(self, session_id : int):
        try:
            self.cur.execute("""DELETE FROM sessions
                                WHERE session_id = ?;""", (session_id,))
            
            self.conn.commit()
            return self.cur.rowcount > 0
        
        except sqlite3.Error as e:
            print(f"DB error: {e}")
            return False


    def edit_session(self, session_id : int=None, activity: str=None, duration: int=None, date: str=None, notes :str=None):

        if not isinstance(session_id, int):
            raise TypeError("session_id must be int")
        if not isinstance(activity, str):
            raise TypeError("activity must be str")
        if not isinstance(duration, int):
            raise TypeError("duration must be int")
        if not isinstance(date, str):
            raise TypeError("date must be str")
        if not isinstance(notes, str):
            raise TypeError("notes must be str")
        
        try:
            if session_id is None:
                return False
            
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
            return self.cur.rowcount > 0
        
        except sqlite3.Error as e:
            print(f"DB error: {e}")
            return False

    
    def read_session(self, session_id=None):

        if session_id is not None:
            res = self.cur.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        else:
            res = self.cur.execute("SELECT * FROM sessions")
          
        return [dict(row) for row in res.fetchall()]
    
    def close(self):
        self.conn.close()


