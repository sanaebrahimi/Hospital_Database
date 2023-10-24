# business logic
import dataaccess as da

# connecting to the database
my_db = da.DataBaseManagement('three_layered_db.db')

import tkinter as tk
import bcrypt
import sqlite3
from tkinter import messagebox as mb

class User:

    def __init__(self, email, password, type):

        # self.username = username
        self.email = email
        self.user_type = type
        self.password = password
        self.hashed_pw = self.make_password_hash()
        print(self.hashed_pw)

    def __str__(self):
        if self.user_type == "patient":
            user = my_db.show(f"""
                                SELECT FirstName, LastName FROM LogIn, Patient WHERE Patient.username = LogIn.username
                                """).pop()[0]
        if self.user_type == "nurse":
            user = my_db.show(f"""
                                SELECT FirstName, LastName FROM LogIn, Nurse WHERE Nurse.username = LogIn.username
                                """).pop()[0]
        return user

    # inserting a query into the database
    def make_password_hash(self):
        hash = bcrypt.hashpw(password= self.password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    def is_password_valid(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def insert(self):
        check_user_existance = False
        try:
            my_db.insert(f"""INSERT INTO LogIn (email_address, password, user_type) VALUES \
                                        ("{self.email}", "{self.hashed_pw}", "{self.user_type}")""")

        except IndexError:
            check_user_existance = False

        # if check_user_existance:
        #     my_db.insert(f"""INSERT INTO LogIn (username, email_address, password, user_type) VALUES \
        #                     ("{self.username}", "{self.email}", "{self.hashed_pw}", "{self.user_type}")""")


        else:
            if self.user_type == "patient":
                user = my_db.show(f"""
                                    SELECT FirstName, LastName FROM LogIn, Patient WHERE Patient.RegistrationID  = LogIn.username
                                    """).pop()[0]
            if self.user_type == "nurse":
                user = my_db.show(f"""
                                    SELECT FirstName, LastName FROM LogIn, Nurse WHERE Nurse.username = LogIn.username
                                    """).pop()[0]

        return check_user_existance

    def get_user(self):

        try:
            if self.is_password_valid():
                user = my_db.show(f"""
                            SELECT * FROM LogIn WHERE email_address="{self.email}"\
                                    AND password= "{self.hashed_pw}" AND username = LogIn.username AND user_type ="{self.user_type} """)
            else:
                mb.showerror("Credential not valid !")
        except:
            mb.showerror("User not found!")
        return user

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