# data access and data storage
import sqlite3


# DataBaseManagement class to insert queries into and select from database

class DataBaseManagement:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.executescript("""
    
            CREATE TABLE IF NOT EXISTS LogIn(
                email_address NVARCHAR(320) PRIMARY KEY,
                password CHAR(60) NOT NULL DEFAULT '',
                user_type text
            );

            CREATE TABLE IF NOT EXISTS Patient(
                SSN integer primary key,
                RegistrationID NVARCHAR(320),
                FirstName text,
                LastName text,
                age integer,
                gender char(6),
                Occupation text,
                Address text,
                Phone integer,
                MedicalHistory text,
                FOREIGN KEY(RegistrationID) REFERENCES LogIn(email_address)     
            );

            CREATE TABLE IF NOT EXISTS Nurse(
                EmployeeID INTEGER,
                username NVARCHAR(320),
                FirstName text,
                LastName text,
                Address text,
                Phone integer,
                Age integer, 
                Gender text,
                PRIMARY KEY(EmployeeID, username),
                FOREIGN KEY(username) REFERENCES LogIn(email_address)
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

    # insert into query
    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    # select from query
    def show(self, query):
        return self.cur.execute(query).fetchall()