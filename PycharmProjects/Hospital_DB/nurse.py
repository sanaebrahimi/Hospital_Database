from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox
import bcrypt
import hospitallogic
from hospitallogic import User
import dataaccess as da
my_db = da.DataBaseManagement('three_layered_db.db')

class Nurse():
    def __init__(self, master: themed_tk.ThemedTk, email):
        self.master = master
        self.master.title('Nurse Homepage')
        self.email = email
        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()






    def enter_info(self):
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)

        self.fname = tk.StringVar()
        ttk.Label(self.inner_frame, text='First Name').grid(row=0, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.fname).grid(row=1, column=0)

        self.lname = tk.StringVar()
        ttk.Label(self.inner_frame, text='Last Name').grid(row=2, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.lname).grid(row=3, column=0)

        self.address = tk.StringVar()
        ttk.Label(self.inner_frame, text='Address').grid(row=4, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.address).grid(row=5, column=0)

        self.age = tk.StringVar()
        ttk.Label(self.inner_frame, text='Age').grid(row=6, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.age).grid(row=7, column=0)

        self.gender = tk.StringVar()
        ttk.Label(self.inner_frame, text="Gender").grid(row=8, column=0, sticky='w')
        ttk.Combobox(self.inner_frame, state="readonly", values=["Male", "Female"], textvariable=self.gender).grid(
            row=9, column=0)
        self.phone = tk.StringVar()
        ttk.Label(self.inner_frame, text="Phone Number").grid(row=10, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.phone).grid(row=11, column=0)

        ttk.Button(self.inner_frame, text='Save', width=18, command = lambda: self.save()).grid(row=12, column=0)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)



    def save(self):

        my_db.insert(f"""INSERT INTO Nurse (username, FirstName, LastName, Address, 
                                   Phone, Age) VALUES \
                                                                ("{self.email}", "{self.fname.get()}","{self.lname.get()}", "{self.address.get()}", "{self.phone.get()}", "{self.age.get()}");""")
        self.inner_frame.destroy()
        self.show()

    def show(self):

        nurse = self.exist()
        if len(nurse) == 0:
            return None
        nurse = nurse.pop()
        inner_frame = tk.LabelFrame(self.master)
        inner_frame.pack(padx=10, pady=10)

        ttk.Label(inner_frame, text= nurse[2] + " " + nurse[3]).grid(row=0, column=0)

        ttk.Label(inner_frame, text=nurse[4]).grid(row=1, column=0)

        ttk.Label(inner_frame, text=nurse[5]).grid(row=2, column=0)

        ttk.Label(inner_frame, text=nurse[6]).grid(row=3, column=0)

        ttk.Button(inner_frame, text='Edit Information', width=18).grid(row=4, column=0)  # command=self.login
        ttk.Button(inner_frame, text='Schedule Appointment', width=18 ).grid(row=5, column=0) #command=self.signup
        ttk.Button(inner_frame, text='Cancel Appointment', width=18).grid(row=6, column=0)  #command=self.signup
        ttk.Button(inner_frame, text='View Schedule', width=18).grid(row=7, column=0) # command=self.signup

        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

        self.frame.destroy()

    def exist(self):
        user = my_db.show(f""" SELECT * FROM Nurse WHERE username ="{self.email}" """)
        return user


