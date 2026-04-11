import unittest
import sqlite3
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from database.core import Database


class TestDB(unittest.TestCase):
        
    def test_sessions_table_created(self):
        db = Database(":memory:")

        db.cur.execute("""
                       SELECT name
                       FROM sqlite_master
                       WHERE type='table' AND name='sessions' """)
        result = db.cur.fetchone()

        self.assertIsNotNone(result, "Таблица не создана.")
        
    def test_add_session(self):
        db = Database(":memory:")

        db.add_session("Gym", 60, "04-10-2026", "Leg day")

        db.cur.execute("""SELECT * FROM sessions""")
        result = db.cur.fetchone()

        self.assertIsNotNone(result, "Пустые данные")

    def test_delete_session(self):
        db = Database(":memory:")
        
        db.add_session("Gym", 60, "04-10-2026", "Leg day")
        db.delete_session(1)

        db.cur.execute("""SELECT * FROM sessions""")
        result = db.cur.fetchone()

        self.assertIsNone(result, "Пустые данные")
        

if __name__ == "__main__":
    unittest.main(exit=False)