import unittest
import sqlite3
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from database.core import Database


class TestDB(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")
        
    def test_sessions_table_created(self):

        self.db.cur.execute("""
                       SELECT name
                       FROM sqlite_master
                       WHERE type='table' AND name='sessions' """)
        result = self.db.cur.fetchone()

        self.assertIsNotNone(result, "Таблица не создана.")
        
    def test_add_session(self):

        self.db.add_session("Gym", 60, "04-10-2026", "Leg day")

        self.db.cur.execute("""SELECT * FROM sessions""")
        result = self.db.cur.fetchone()

        self.assertEqual(result[1], "Gym")
        self.assertEqual(result[2], 60)
        self.assertEqual(result[3], "04-10-2026")
        self.assertEqual(result[4], "Leg day")

    def test_delete_session(self):
        
        self.db.add_session("Gym", 60, "04-10-2026", "Leg day")

        self.db.cur.execute("SELECT session_id FROM sessions")
        session_id = self.db.cur.fetchone()[0]

        self.db.delete_session(session_id)

        self.db.cur.execute("""SELECT * FROM sessions""")
        result = self.db.cur.fetchone()

        self.assertIsNone(result, "Пустые данные")

    def test_delete_nonexistent(self):
        self.db.delete_session(999)
        self.db.cur.execute("SELECT COUNT(*) FROM sessions")
        count = self.db.cur.fetchone()[0]
        self.assertEqual(count, 0)

    def test_edit_full_session(self):
   
        self.db.add_session("Gym", 60, "04-10-2026", "Leg day")

        
        self.db.cur.execute("SELECT session_id FROM sessions")
        session_id = self.db.cur.fetchone()[0]

        self.db.edit_session(session_id, activity="Read a book", 
                        duration=60, 
                        date="04-10-2026 12:00", 
                        notes="Atomic habits")


        self.db.cur.execute("""SELECT * FROM sessions WHERE session_id = (?)""", (session_id,))
        result = self.db.cur.fetchone()

        self.assertEqual(result[0], session_id)
        self.assertEqual(result[1], "Read a book")
        self.assertEqual(result[2], 60)
        self.assertEqual(result[3], "04-10-2026 12:00")
        self.assertEqual(result[4], "Atomic habits")

    def test_read_session(self):

        self.db.add_session("Gym", 60, "04-10-2026", "Leg day")

        result = self.db.read_session()

        self.assertEqual(result[0]["activity"], "Gym")
        self.assertEqual(result[0]["duration_minutes"], 60)
        self.assertEqual(result[0]["session_date"], "04-10-2026")
        self.assertEqual(result[0]["notes"], "Leg day")

    def test_add_session_returns_id(self):
        
        self.db.add_session("Breakfast", 30, "04-21-2026", "Eggs and cottage cheese")

        self.db.cur.execute("SELECT session_id FROM sessions")
        result = self.db.cur.fetchone()[0]

        self.assertIsNotNone(result, "session_id not found")
        

if __name__ == "__main__":
    unittest.main(exit=False)