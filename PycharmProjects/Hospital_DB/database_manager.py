# data access and data storage
import sqlite3


# DataBaseManager class to insert queries into and select from database
# drop table Patient;
# drop table LogIn;
class DataBaseManager:
    def __init__(self, path):
        self.path = path
        conn = sqlite3.connect(self.path)
        conn.cursor().executescript("""
            
            CREATE TABLE IF NOT EXISTS LogIn(
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Patient(
                patient_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                SSN INTEGER NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                race TEXT NOT NULL,
                occupation TEXT NOT NULL,
                address TEXT NOT NULL,
                phone INTEGER NOT NULL,
                medical_history TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES LogIn(user_id)
            );

            CREATE TABLE IF NOT EXISTS Nurse(
                employee_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                address TEXT NOT NULL,
                phone INTEGER NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES LogIn(user_id)
            );

            CREATE TABLE IF NOT EXISTS Vaccine(
                VaccName text primary key,
                Available_Dose integer,
                OnHold_Dose integer,
                CompanyName REFERENCES Company(name)
            );

            CREATE TABLE IF NOT EXISTS Company(
                name text primary key,
                products text
            );
        """)
        conn.close()

    # insert into query
    def insert(self, query) -> None:
        conn = sqlite3.connect(self.path)
        conn.cursor().execute(query)
        conn.commit()
        conn.close()

    # select from query
    def select(self, query) -> list:
        conn = sqlite3.connect(self.path)
        selection = conn.cursor().execute(query).fetchall()
        conn.close()
        return selection