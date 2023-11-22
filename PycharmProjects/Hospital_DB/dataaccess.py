# data access and data storage
import sqlite3


# DataBaseManagement class to insert queries into and select from database
# drop table Nurse;
#            drop table Patient;
#            # drop table LogIn;
# drop table NurseSchedule;
# drop table Nurse;
# drop table Patient;
# drop table LogIn;
class DataBaseManagement:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

        self.cur.executescript("""
            
            
            CREATE TABLE IF NOT EXISTS LogIn(
                user_id INTEGER,
                email_address TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL,
                PRIMARY KEY(user_id, email_address)
            );

            CREATE TABLE IF NOT EXISTS Patient(
                SSN integer,
                username NVARCHAR(320),
                RegistrationID NVARCHAR(320),
                FirstName text,
                LastName text,
                age integer,
                gender char(6),
                Race text,
                Occupation text,
                Address text,
                Phone integer,
                MedicalHistory text,
                PRIMARY KEY(username),
                FOREIGN KEY(RegistrationID) REFERENCES LogIn(email_address) on delete cascade    
            );

            CREATE TABLE IF NOT EXISTS Nurse(
                EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                FirstName text,
                LastName text,
                Address text,
                Phone integer,
                Age integer, 
                Gender text,
                FOREIGN KEY(username) REFERENCES LogIn(email_address) on delete cascade
            );

            CREATE TABLE IF NOT EXISTS Vaccine(

                VaccName text primary key,
                Available_Dose integer,
                OnHold_Dose integer,
                CompanyName REFERENCES Company(name) on delete cascade     
            );

            CREATE TABLE IF NOT EXISTS Company(

                name text primary key,
                products text
            );
            CREATE TABLE IF NOT EXISTS NurseSchedule(
                id integer primary key AUTOINCREMENT,
                EmployeeID INTEGER,
                email text,
                date text,
                time text,
                FOREIGN KEY(EmployeeID) REFERENCES Nurse(EmployeeID) on delete cascade,
                FOREIGN KEY(email) REFERENCES Nurse(username) on delete cascade
            );

        """)

    # insert into query
    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    # select from query
    def show(self, query):
        return self.cur.execute(query).fetchall()