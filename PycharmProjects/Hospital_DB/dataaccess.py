# data access and data storage
import sqlite3


# DataBaseManagement class to insert queries into and select from database

class DataBaseManagement:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS LogIn(
                username INTEGER PRIMARY KEY AUTOINCREMENT,
                email_address NVARCHAR(320),
                password CHAR(60) NOT NULL DEFAULT '',
                user_type text
            );
            CREATE TABLE IF NOT EXISTS Patient(

                SSN integer primary key,
                RegistrationID REFERENCES LogIn(username),
                FirstName text,
                LastName text,
                age integer,
                gender char(6),
                Occupation text,
                Address text,
                Phone integer,
                MedicalHistory text
                
            );

            CREATE TABLE IF NOT EXISTS Nurse(

                EmployeeID integer primary key,
                username REFERENCES LogIn(username),
                FirstName text,
                LastName text,
                Address text,
                Phone integer,
                Age integer
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
        self.cur.executescript("""

            CREATE TABLE IF NOT EXISTS Customer (

                CustomerId integer primary key,
                CustomerFirstName text,
                CustomerLastName text
            );

            CREATE TABLE IF NOT EXISTS Basket(

                BasketId integer primary key,
                OrderDate text,
                SumPrice float,
                CustomerId REFERENCES Customer (CustomerId)
            );

            CREATE TABLE IF NOT EXISTS Product(

                ProductId integer primary key,
                ProductName text
            );

            CREATE TABLE IF NOT EXISTS Product_Price(

                ProductPriceId integer primary key,
                ProductId REFERENCES Product (ProductId),
                ProductPrice float
            );

            CREATE TABLE IF NOT EXISTS Basket_Product(

                BasketProductId integer primary key,
                ProductId REFERENCES Product (ProductId),   
                BasketId REFERENCES Basket (BasketId)

            );

            INSERT INTO Product (ProductName) VALUES ('Bag');
            INSERT INTO Product (ProductName) VALUES ('T-shirt');
            INSERT INTO Product (ProductName) VALUES ('Pants');
            INSERT INTO Product (ProductName) VALUES ('Cap');

            INSERT INTO Product_Price (ProductId, ProductPrice) VALUES (1, 805000);
            INSERT INTO Product_Price (ProductId, ProductPrice) VALUES (2, 140000);
            INSERT INTO Product_Price (ProductId, ProductPrice) VALUES (3, 340000);
            INSERT INTO Product_Price (ProductId, ProductPrice) VALUES (4, 110000);

        """)

    # insert into query
    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    # select from query
    def show(self, query):
        return self.cur.execute(query).fetchall()