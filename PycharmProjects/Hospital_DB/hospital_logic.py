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
            self.db.insert(f"""INSERT INTO LogIn (username, password, user_type)
                VALUES ("{username}", "{password}", "Patient");""")
            
            user_id = self.get_user_info(username=username, user_type="Patient")["user_id"]

            self.db.insert(f"""INSERT INTO Patient (user_id, SSN, firstname, lastname, age,
                           gender,race, occupation, address, phone, medical_history)
                           VALUES ("{user_id}", "{SSN}", "{firstname}", "{lastname}", "{age}", "{gender}",
                           "{race}", "{occupation}", "{address}", "{phone}", "{medical_history}");""")
            
            print(f"""Signed up patient with user_id: {user_id}...""")
        except:
            print("ERROR: _insert_user() failed!")

    # Signs up an admin by inserting its user info
    def admin_signup(self, username, password) -> None:
        print("Signing up admin...")
        try:
            self.db.insert(f"""INSERT INTO LogIn (username, password, user_type)
                VALUES ("{username}", "{password}", "Admin");""")
            
            user_id = self.get_admin_info()["user_id"]
            
            print(f"""Signed up admin with user_id: {user_id}...""")
        except:
            print("ERROR: _insert_user() failed!")

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
            selection = self.db.select(f""" SELECT * FROM LogIn WHERE username="{username}" AND user_type="{user_type}" """)
            fields = ["user_id", "username", "password", "user_type"]
            return self._parse_row(selection=selection, fields=fields)
        except:
            print("ERROR: get_user_info() failed!")

    # Searches the LogIn table for the admin user
    def get_admin_info(self) -> dict:
        try:
            print("Getting admin info...")
            selection = self.db.select("""SELECT * FROM LogIn WHERE user_type="Admin" """)
            fields = ["user_id", "username", "password", "user_type"]
            return self._parse_row(selection=selection, fields=fields)
        except:
            print("ERROR: get_admin_info() failed!")