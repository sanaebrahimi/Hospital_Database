# business logic
import dataaccess as da

# connecting to the database
my_db = da.DataBaseManagement('three_layered_db.db')
import tkinter as tk
import bcrypt
import sqlite3
from tkinter import messagebox as mb
# secret_key = bcrypt.gensalt(12)
class User:

    def __init__(self, email, password, type):

        # self.username = username
        self.email = email
        self.user_type = type
        self.password = password
        self.hashed_pw = self.make_password_hash()

    def __str__(self):
        user = []
        if self.user_type == "patient":
            user = my_db.show(f"""
                                SELECT FirstName, LastName FROM LogIn, Patient WHERE Patient.username = LogIn.username
                                """).pop()[0]

        if self.user_type == "nurse":
            user = my_db.show(f"""
                                SELECT FirstName, LastName FROM LogIn, Nurse WHERE Nurse.username = LogIn.username
                                """).pop()[0]
        return user[0] + user[1]

    # inserting a query into the database
    def make_password_hash(self):
        hash = bcrypt.hashpw(password= self.password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    def is_password_valid(self, hash, password):
        print(password.encode('utf-8'))
        pas = bcrypt.checkpw(password.encode('utf-8'), hash)

        return pas

    def insert(self):
        print("Signing up...")
        try:
            my_db.insert(f"""INSERT INTO LogIn (email_address, password, user_type) VALUES \
                                        ("{self.email}", "{self.hashed_pw}", "{self.user_type}");""")

        except IndexError:
            if self.user_type == "patient":
                user = my_db.show(f"""
                                    SELECT FirstName, LastName FROM LogIn, Patient WHERE Patient.RegistrationID  = LogIn.username
                                    """).pop()[0]
            if self.user_type == "nurse":
                user = my_db.show(f"""
                                    SELECT FirstName, LastName FROM LogIn, Nurse WHERE Nurse.username = LogIn.username
                                    """).pop()[0]

    # showing the queries inserted by the user
    @staticmethod
    def show():
        q = my_db.show(f"""
                SELECT c.CustomerFirstName, c.CustomerLastName, p.ProductName, pp.ProductPrice FROM Customer as c \
                INNER JOIN Basket as b ON c.CustomerId=b.CustomerId INNER JOIN Basket_Product as bp ON b.BasketId=bp.BasketId 
                INNER JOIN Product as p ON p.ProductId = bp.ProductId INNER JOIN Product_Price as pp ON 
                pp.ProductId=p.ProductId;
            """)

        return q

    # showing what are the products a customer has bought
    @staticmethod
    def show_history(fullname):
        q = my_db.show(f"""SELECT p.ProductName, pp.ProductPrice FROM Customer as c \
            INNER JOIN Basket as b ON c.CustomerId=b.CustomerId INNER JOIN Basket_Product as bp ON b.BasketId=bp.BasketId 
            INNER JOIN Product as p ON p.ProductId = bp.ProductId INNER JOIN Product_Price as pp ON 
            pp.ProductId=p.ProductId WHERE c.CustomerFirstName="{fullname[0]}" AND c.CustomerLastName="{fullname[1]}"
            """)
        return q

def get_user( email, user_type):

    try:

            # if self.is_password_valid():
                # print(my_db.show(f"""
                #             SELECT * FROM LogIn WHERE email_address="{self.email}" AND user_type ="{self.user_type} " """))
            # password = '9i2309180943'
            # bytes = password.encode('utf-8')
            # salt = bcrypt.gensalt()
            # hash = bcrypt.hashpw(bytes, salt)
            # userPassword = '9i2309180943'
            # result = bcrypt.checkpw(userPassword.encode('utf-8'), hash)
            # print(result)

        user = my_db.show(f""" SELECT * FROM LogIn WHERE email_address="{email}" AND user_type ="{user_type}" """)
        print(my_db.show(f""" SELECT * FROM LogIn """))
            # if self.is_password_valid(user[0][2], password):
            #     print(self.user_type)
        return user

            # else:
            #     mb.showerror("Password not valid!")
            #     return None

    except:
        print("Error Occured!")