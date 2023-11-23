import database_manager as dm
import bcrypt

class HospitalLogic:
    def __init__(self):
        self.db = dm.DataBaseManager('three_layered_db.db')

    def _get_hash(self, password: str) -> str:
        hash = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    def is_password_valid(self, password, hash) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

    def patient_signup(self, user_dict: dict):
        print("Signing up patient...")
        try:
            self.db.insert(f"""INSERT INTO LogIn (username, password, user_type) VALUES
                           ("{user_dict["username"]}", "{self._get_hash(user_dict["password"])}", "Patient");""")
            user_id = self.get_user_info(username=user_dict["username"], user_type="Patient")["user_id"]
            self.db.insert(f"""INSERT INTO Patient (user_id, SSN, firstname, 
                           lastname, age, gender,
                           race, occupation, address,
                           phone, medical_history) VALUES
                           ("{user_id}", "{user_dict["SSN"]}", "{user_dict["firstname"]}",
                           "{user_dict["lastname"]}", "{user_dict["age"]}", "{user_dict["gender"]}",
                           "{user_dict["race"]}", "{user_dict["occupation"]}", "{user_dict["address"]}",
                           "{user_dict["phone"]}", "{user_dict["medical_history"]}")""")
            print(f"""Signed up user_id: {user_id}...""")
        except IndexError:
            print("ERROR: patient_signup() failed.")

    def show(self, query) -> list:
        selection = self.db.select(query)
        print(selection)
        return selection

    def get_user_info(self, username: str, user_type: str) -> dict:
        try:
            print("Getting user_info...")
            selection = self.db.select(f""" SELECT * FROM LogIn WHERE username="{username}" AND user_type="{user_type}" """)
            user_dict = {}
            if (0 < len(selection)):
                row = selection.pop(0)
                user_columns = ["user_id", "username", "password", "user_type"]
                for field in range(0, len(row)):
                    user_dict[user_columns[field]] = row[field]
            return user_dict
        except:
            print("ERROR:  get_user_info() failed!")