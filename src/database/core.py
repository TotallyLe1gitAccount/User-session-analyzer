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
        
        if notes is not None:
            if not isinstance(notes, str):
                raise TypeError("notes must be str")

        
        self.cur.execute("""INSERT INTO sessions (activity, duration_minutes, session_date, notes)
                            VALUES (?, ?, ?, ?)""", (activity, duration, date, notes))
            

        self.conn.commit()
        return self.cur.lastrowid
        


    def delete_session(self, session_id : int):

        if not isinstance(session_id, int):
            raise TypeError("session_id must be int")
        
        try:
            self.cur.execute("""DELETE FROM sessions
                                WHERE session_id = ?;""", (session_id,))
            
            self.conn.commit()
        
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error {e}") from e
        
        return self.cur.rowcount


    def edit_session(self, session_id : int=None, activity: str=None, duration: int=None, date: str=None, notes :str=None):
        
        if session_id is None:
            raise ValueError("session_id must be not empty")
        

        if not isinstance(session_id, int):
            raise TypeError("session_id must be int")
        
        fields = []
        values = []

        if activity is not None:
            if not isinstance(activity, str):
                raise TypeError("activity must be str")
            fields.append("activity = ?")
            values.append(activity)

        if duration is not None:
            if not isinstance(duration, int):
                raise TypeError("duration must be int")
            fields.append("duration_minutes = ?")
            values.append(duration)

        if date is not None:
            if not isinstance(date, str):
                raise TypeError("date must be str")
            fields.append("session_date = ?")
            values.append(date)

        if notes is not None:
            if not isinstance(notes, str):
                raise TypeError("notes must be str")
            fields.append("notes = ?")
            values.append(notes)

        if not fields:
            raise ValueError("no fields to update")

        values.append(session_id)
    
        query = f"""
            UPDATE sessions
            SET {", ".join(fields)}
            WHERE session_id = ?
        """

        self.cur.execute(query, tuple(values))
        self.conn.commit()
        return self.cur.rowcount
        
    
    def get_session(self, session_id):

        if not isinstance(session_id, int):
            raise TypeError("session_id must be int")
        
        res = self.cur.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = res.fetchone()
        
        return dict(row) if row else None
    
    def get_all_sessions(self):

        res = self.cur.execute("SELECT * FROM sessions")
        rows = [dict(row) for row in res.fetchall()]

        return rows

    
    def close(self):
        self.conn.close()

