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
        

if __name__ == "__main__":
    unittest.main(exit=False)