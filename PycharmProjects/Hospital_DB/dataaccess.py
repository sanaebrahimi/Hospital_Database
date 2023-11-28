import sqlite3


# DataBaseManagement class to insert queries into and select from database
# CREATE TABLE IF NOT EXISTS Hospital(
#
#                 schedule_id integer primary key AUTOINCREMENT,
#                 numberof_patients_per_slot integer DEFAULT 0 NOT NULL,
#                 date text,
#                 time text
#
#             );
# drop table NurseSchedule;
              # drop table Nurse;
              # drop table Hospital;
              # drop table Patient;
              # drop table LogIn;
class DataBaseManagement:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

        self.cur.executescript("""
            drop table VaccineSchedule;
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
            
            CREATE TABLE IF NOT EXISTS VaccineSchedule(
                appointment_id integer primary key AUTOINCREMENT,
                schedule_id integer,
                registration_id NVARCHAR(320),
                NursePractioner integer,
                vaccine_name text,
                date text,
                time text,
                FOREIGN KEY(vaccine_name) REFERENCES Vaccine(VaccName) on delete cascade,
                FOREIGN KEY(NursePractioner) REFERENCES Nurse(EmployeeID) on delete cascade,
                FOREIGN KEY(schedule_id) REFERENCES NurseSchedule(id) on delete cascade,
                FOREIGN KEY(registration_id) REFERENCES Patient(RegistrationID) on delete cascade


            );
            CREATE TABLE IF NOT EXISTS NurseSchedule(
                id integer primary key AUTOINCREMENT,
                EmployeeID INTEGER,
                email text,
                date text,
                time text,
                numberof_patients_per_nurse integer DEFAULT 0 NOT NULL,
                FOREIGN KEY(EmployeeID) REFERENCES Nurse(EmployeeID) on delete cascade,
                FOREIGN KEY(email) REFERENCES Nurse(username) on delete cascade,
                CHECK(numberof_patients_per_nurse<= 12)
                );
          
            CREATE TRIGGER IF NOT EXISTS check_numberof_patients_scheduled
                AFTER INSERT ON VaccineSchedule
            BEGIN
                SELECT
                    CASE
	                    WHEN (SELECT SUM(numberof_patients_per_nurse) from NurseSchedule WHERE New.date = date AND New.time = time) == 100 THEN
   	                        RAISE (ABORT,'100 patients for this time slot')
                    END;
            END;
            CREATE TRIGGER IF NOT EXISTS check_nurses_email
            BEFORE INSERT ON Nurse 
            BEGIN
            SELECT CASE 
            WHEN 
                (NEW.username IN
                (SELECT
                    Nurse.username from Nurse
                    WHERE 
                    NEW.username = Nurse.username))
                    THEN
   	                RAISE (ABORT,'This email already exists!')
   	                END;          
            END;



        """)

    # insert into query
    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    # select from query
    def show(self, query):
        return self.cur.execute(query).fetchall()
