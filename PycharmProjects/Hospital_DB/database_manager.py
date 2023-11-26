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
                UserID INTEGER PRIMARY KEY,
                Username TEXT NOT NULL,
                Password TEXT NOT NULL,
                UserType TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Patient(
                PatientID INTEGER PRIMARY KEY,
                UserID INTEGER,
                SSN INTEGER NOT NULL,
                FirstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                Age INTEGER NOT NULL,
                Gender TEXT NOT NULL,
                Race TEXT NOT NULL,
                Occupation TEXT NOT NULL,
                Address TEXT NOT NULL,
                Phone INTEGER NOT NULL,
                MedicalHistory TEXT NOT NULL,
                FOREIGN KEY(UserID) REFERENCES LogIn(UserID)
            );

            CREATE TABLE IF NOT EXISTS Nurse(
                EmployeeID INTEGER PRIMARY KEY,
                UserID INTEGER,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Address TEXT NOT NULL,
                Phone INTEGER NOT NULL,
                Age INTEGER NOT NULL,
                Gender TEXT NOT NULL,
                FOREIGN KEY(UserID) REFERENCES LogIn(UserID)
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
    def select(self, query) -> list[tuple]:
        conn = sqlite3.connect(self.path)
        selection = conn.cursor().execute(query).fetchall()
        conn.close()
        return selection