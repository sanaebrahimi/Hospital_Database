import os
import sqlite3
from sqlite3 import Error

class database:
    def __init__(self, filename: str) -> None:
        self.dbfilename = filename
        conn = self.create_connection()
        self.add_tables(conn)
        conn.close()

    def add_tables(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS LogIn(
                user_id INTEGER PRIMARY KEY,
                email_address TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Patient(
                patient_id INTEGER PRIMARY KEY,
                ssn INTEGER NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                occupation TEXT NOT NULL,
                address TEXT NOT NULL,
                phone INTEGER NOT NULL,
                medical_history TEXT NOT NULL
                
            );
            """)

    def create_connection(self) -> sqlite3.Connection:
        conn = None
        try:
            conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + self.dbfilename)
            return conn
        except Error as e:
            print(e)
            return None