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

    # Parses the first row/tuple in the selection list into a dictionary with the given fields
    def _parse_row(self, selection: list[tuple], fields: list) -> dict:
        field_dict = {}
        if (0 != len(selection)):
            for field in range(0, len(fields)):
                field_dict[fields[field]] = selection[0][field]
        return field_dict

    # Searches the LogIn table for a user with the given username and user_type and returns all fields
    def get_user_info(self, username: str, user_type: str) -> dict:
        try:
            print("Getting user_info...")
            selection = self.db.select(f""" SELECT * FROM LogIn WHERE Username="{username}" AND UserType="{user_type}" """)
            fields = ["UserID", "Username", "Password", "UserType"]
            return self._parse_row(selection=selection, fields=fields)
        except:
            print("ERROR: get_user_info() failed!")

    # Searches the LogIn table for the admin user
    def get_admin_info(self) -> dict:
        try:
            print("Getting admin info...")
            selection = self.db.select("""SELECT * FROM LogIn WHERE UserType="Admin" """)
            fields = ["UserID", "Username", "Password", "UserType"]
            return self._parse_row(selection=selection, fields=fields)
        except:
            print("ERROR: get_admin_info() failed!")