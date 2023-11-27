import database_manager as dm
import bcrypt

class HospitalLogic:
    def __init__(self):
        self.db = dm.DataBaseManager('three_layered_db.db')

    # Converts the given password to the hashed version for storage
    def _get_hash(self, password) -> str:
        return bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')

    # Returns true if the given password from the user matches the stored hashed password
    def is_password_valid(self, password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

    # Signs up a patient by inserting its user and patient info
    def patient_signup(self, username, password, SSN, firstname, lastname, age, gender,
                       race, occupation, address, phone, medical_history) -> None:
        print("Signing up patient...")
        try:
            self.db.insert(f"""INSERT INTO LogIn (Username, Password, UserType)
                VALUES ("{username}", "{password}", "Patient");""")
            
            user_id = self.get_user_info(username=username, user_type="Patient")["UserID"]

            self.db.insert(f"""INSERT INTO Patient (UserID, SSN, Firstname, Lastname, Age,
                           Gender, Race, Occupation, Address, Phone, MedicalHistory)
                           VALUES ("{user_id}", "{SSN}", "{firstname}", "{lastname}", "{age}", "{gender}",
                           "{race}", "{occupation}", "{address}", "{phone}", "{medical_history}");""")
            
            print(f"""Signed up patient with UserID: {user_id}...""")
        except:
            print("ERROR: patient_signup() failed!")

    # Signs up an admin by inserting its user info
    def admin_signup(self, username, password) -> None:
        print("Signing up admin...")
        try:
            self.db.insert(f"""INSERT INTO LogIn (Username, Password, UserType)
                VALUES ("{username}", "{self._get_hash(password)}", "Admin");""")
            
            user_id = self.get_admin_info()["UserID"]
            
            print(f"""Signed up admin with UserID: {user_id}...""")
        except:
            print("ERROR: admin_signup() failed!")

    # Signs up a nurse by inserting its user and nurse info
    def nurse_signup(self, username, password, firstname, lastname, address, phone, age, gender) -> None:
        print("Signing up nurse...")
        try:
            self.db.insert(f"""INSERT INTO LogIn (Username, Password, UserType)
                VALUES ("{username}", "{password}", "Nurse");""")
            
            user_id = self.get_user_info(username=username, user_type="Nurse")["UserID"]

            self.db.insert(f"""INSERT INTO Nurse (UserID, FirstName, LastName, Address, Phone, Age, Gender)
                           VALUES ("{user_id}", "{firstname}", "{lastname}","{address}","{phone}", "{age}", "{gender}");""")
            
            print(f"""Signed up nurse with UserID: {user_id}...""")
        except:
            print("ERROR: nurse_signup() failed!")

    # Searches the LogIn table for a user with the given username and user_type and returns all fields
    def get_user_info(self, username: str, user_type: str) -> dict:
        try:
            print("Getting user_info...")
            selection = self.db.select_dicts(f""" SELECT * FROM LogIn WHERE Username="{username}" AND UserType="{user_type}" """)
            if(0 == len(selection)):
                return {}
            else:
                return selection[0]
        except:
            print("ERROR: get_user_info() failed!")

    # Gets the fields of the admin user
    def get_admin_info(self) -> dict:
        try:
            print("Getting admin info...")
            selection = self.db.select_dicts("""SELECT * FROM LogIn WHERE UserType="Admin" """)
            if(0 == len(selection)):
                return {}
            else:
                return selection[0]
        except:
            print("ERROR: get_admin_info() failed!")

    # Gets a list of all nurses in the database
    def get_nurses(self) -> list[dict]:
        try:
            print("Getting nurses...")
            nurses = self.db.select_dicts("""SELECT * FROM Nurse JOIN LogIn ON Nurse.UserID=LogIn.UserID """)
            return nurses
        except:
            print("ERROR: get_nurses() failed!")

    # Gets a list of all vaccines in the database
    def get_vaccines(self) -> list[dict]:
        try:
            print("Getting vaccines...")
            vaccines = self.db.select_dicts("""SELECT * FROM Vaccine """)
            return vaccines
        except:
            print("ERROR: get_vaccines() failed!")
    
    def add_vaccine(self, CompanyName, VaccineName) -> None:
        print("Adding Vaccine...")
        try:
            self.db.insert(f"""INSERT INTO Vaccine (CompanyName, VaccineName, Available_Doses, OnHold_Doses)
                           VALUES ("{CompanyName}", "{VaccineName}", "0", "0"); """)
        except:
            print("ERROR: add_vaccine() failed!")