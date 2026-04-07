import sqlite3

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()



