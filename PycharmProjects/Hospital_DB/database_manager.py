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
                VaccineID INTEGER PRIMARY KEY,
                CompanyName TEXT NOT NULL,
                VaccineName TEXT NOT NULL,
                Available_Doses INTEGER NOT NULL,
                OnHold_Doses INTEGER NOT NULL
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
    
    def select_dicts(self, query) -> list[dict]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        selection = conn.cursor().execute(query).fetchall()
        conn.close()
        retlist = []
        if(0 != len(selection)):
            column_names = selection[0].keys()
            for row in selection:
                rowdict = {}
                for field in column_names:
                    rowdict[field] = row[field]
                retlist.append(rowdict)
        return retlist
