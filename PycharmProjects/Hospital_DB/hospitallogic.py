# business logic
import dataaccess as da

# connecting to the database
my_db = da.DataBaseManagement('three_layered_db.db')
import bcrypt
class User:
    def __init__(self, email, password, type):
        # self.username = username
        self.email = email
        self.user_type = type
        self.password = password
        self.hashed_pw = self.make_password_hash()
        # self.insert(f"""INSERT INTO LogIn (email_address, password, user_type) VALUES \
        #                                                 ("admin2023@uic.edu", "{self.hashed_pw}", "{self.user_type}");""")


    def make_password_hash(self):
        hash = bcrypt.hashpw(password= self.password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    def is_password_valid(self, hash, password):
        pas = bcrypt.checkpw(password.encode('utf-8'), hash)
        return pas

    # inserting a query into the database
    def insert(self, query=None):
        try:
            my_db.insert(f"""INSERT INTO LogIn (email_address, password, user_type) VALUES \
                                        ("{self.email}", "{self.hashed_pw}", "{self.user_type}");""")
        except:
            print("ERROR: insert() failed!")

    # showing the queries inserted by the user
    def show(self, query):
        return my_db.show(query)


def get_user(email, user_type):

    try:
        user = my_db.show(f""" SELECT * FROM LogIn WHERE email_address="{email}" AND user_type ="{user_type}" """)
        return user
    except:
        print("Error Occured!")