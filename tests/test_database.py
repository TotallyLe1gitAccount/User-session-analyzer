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

        id = self.db.add_session("Foo", 900, "01-01-1000", "Bar")
    
        result_read = self.db.get_session(id)

        self.assertEqual(result_read["activity"], "Foo")
        self.assertEqual(result_read["duration_minutes"], 900)
        self.assertEqual(result_read["session_date"], "01-01-1000")
        self.assertEqual(result_read["notes"], "Bar")
        
       
    def test_add_row_instances(self):

        result_add = self.db.add_session("Foo", 900, "01-01-1000", "Bar")
        self.assertIsInstance(result_add, int)
        

    def test_add_row_invalid_instances(self):

        with self.assertRaises(TypeError):
            self.db.add_session(900, "Foo", [], {})


    def test_delete_session(self):
        
        result_add = self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        result_delete = self.db.delete_session(result_add)

        self.assertTrue(result_delete)

        result_read = self.db.get_all_sessions()

        self.assertEqual(result_read, [])

        
    def test_delete_nonexistent(self):

        self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        result_delete = self.db.delete_session(999)
        
        self.assertFalse(result_delete)

        result_read = self.db.get_all_sessions()

        self.assertEqual(result_read[0]["activity"], "Foo")
        self.assertEqual(result_read[0]["duration_minutes"], 900)
        self.assertEqual(result_read[0]["session_date"], "01-01-1000")
        self.assertEqual(result_read[0]["notes"], "Bar")


    def test_edit_full_session(self):
   
        result_add = self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        result_edit = self.db.edit_session(result_add, activity="FooBar", 
                        duration=901, 
                        date="04-10-2026 12:00", 
                        notes="BarFoo")

        self.assertEqual(result_edit, 1)

        result_read = self.db.get_session(result_add)

        self.assertEqual(result_read["activity"], "FooBar")
        self.assertEqual(result_read["duration_minutes"], 901)
        self.assertEqual(result_read["session_date"], "04-10-2026 12:00")
        self.assertEqual(result_read["notes"], "BarFoo")

    
    def test_edit_nonexistent(self):
        
        result_add = self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        result_edit = self.db.edit_session(result_add + 1, activity="Foo", duration=905, date="01-01-1000", notes="")


        self.assertEqual(result_edit, 0)


    def test_edit_single_input(self):
            
            result_add = self.db.add_session("Foo", 900, "01-01-1000", "Bar")

            result_edit = self.db.edit_session(result_add, activity="FooBar")

            self.assertEqual(result_edit, 1)

            result_read = self.db.get_session(result_add)
            

            self.assertEqual(result_read["activity"], "FooBar")
            self.assertEqual(result_read["duration_minutes"], 900)
            self.assertEqual(result_read["session_date"], "01-01-1000")
            self.assertEqual(result_read["notes"], "Bar")


    def test_edit_session_invalid_instance(self):

        self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        with self.assertRaises(TypeError):
            self.db.edit_session('f', activity=9, 
                duration='901', 
                date="04-10-2026 12:00", 
                notes=112)

 
    def test_add_session_returns_id(self):

        id = self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        self.assertIsNotNone(id)
        self.assertIsInstance(id, int)


    def test_get_all_session_returns_valid_structures(self):

        self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        result = self.db.get_all_sessions()

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        session = result[0]

        self.assertIsInstance(session, dict)


    def test_get_session_not_found(self):

        self.db.add_session("Foo", 900, "01-01-1000", "Bar")

        read_session = self.db.get_session(999)

        self.assertEqual(read_session, None)
    

if __name__ == "__main__":
    unittest.main(exit=False)