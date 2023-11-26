from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox
import bcrypt
import hospital_logic
from hospital_logic import User
import dataaccess as da
my_db = da.DataBaseManagement('three_layered_db.db')

class Patient():
    def __init__(self, master: themed_tk.ThemedTk, email):
        self.master = master
        self.master.title('Patient Homepage')
        self.reg_id = email
        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()






    def enter_info(self, user=None):

        self.frame.destroy()
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)

        self.fname = tk.StringVar()
        ttk.Label(self.inner_frame, text='First Name').grid(row=0, column=0, sticky='w')
        box1 = ttk.Entry(self.inner_frame, textvariable=self.fname)
        box1.grid(row=1, column=0)
        box1.insert(0,user[3])

        self.lname = tk.StringVar()
        ttk.Label(self.inner_frame, text='Last Name').grid(row=2, column=0, sticky='w')
        box2 = ttk.Entry(self.inner_frame, textvariable=self.lname)
        box2.grid(row=3, column=0)
        box2.insert(0, user[4])

        self.address = tk.StringVar()
        ttk.Label(self.inner_frame, text='Address').grid(row=0, column=1, sticky='w')
        box3 = ttk.Entry(self.inner_frame, textvariable=self.address)
        box3.grid(row=1, column=1)
        box3.insert(0, user[9])

        self.age = tk.StringVar()
        ttk.Label(self.inner_frame, text='Age').grid(row=2, column=1, sticky='w')
        box4 = ttk.Entry(self.inner_frame, textvariable=self.age)
        box4.grid(row=3, column=1)
        box4.insert(0, user[5])

        self.gender = tk.StringVar()
        ttk.Label(self.inner_frame, text="Gender").grid(row=8, column=0, sticky='w')
        box5 = ttk.Combobox(self.inner_frame, state="readonly", values=["Male", "Female"], textvariable=self.gender)
        box5.grid(row=9, column=0)
        curr = ["Male", "Female"].index(user[6])
        box5.current(curr)

        self.race = tk.StringVar()
        ttk.Label(self.inner_frame, text="Race").grid(row=8, column=1, sticky='w')
        box6 = ttk.Combobox(self.inner_frame, state="readonly", values=[" ","Hispanic", "African American", "White"], textvariable=self.race)
        box6.grid(row=9, column=1)
        curr = ['',"Hispanic", "African American", "White"].index(user[7])
        box6.current(curr)

        self.phone = tk.StringVar()
        ttk.Label(self.inner_frame, text="Phone Number").grid(row=10, column=0, sticky='w')
        box7 = ttk.Entry(self.inner_frame, textvariable= self.phone)
        box7.grid(row=11, column=0) #self.phone
        box7.insert(0, user[10])

        self.ssn = tk.StringVar()
        ttk.Label(self.inner_frame, text="SSN").grid(row=10, column=1, sticky='w')
        box8 = ttk.Entry(self.inner_frame, textvariable=self.ssn)
        box8.grid(row=11, column=1)
        box8.insert(0, user[0])

        self.job = tk.StringVar()
        ttk.Label(self.inner_frame, text='Occupation').grid(row=16, column=0, sticky='w')
        box9 = ttk.Entry(self.inner_frame, textvariable=self.job)
        box9.grid(row=17, column=0)
        box9.insert(0, user[8])

        self.history = tk.StringVar()
        ttk.Label(self.inner_frame, text='Medical History').grid(row=16, column=1, sticky='w')
        box10 = ttk.Entry(self.inner_frame, textvariable=self.history)
        box10.grid(row=17, column=1)
        box10.insert(0, user[11])

        ttk.Button(self.inner_frame, text='Save', width=18, command = lambda: self.save()).grid(row=20, column=1)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)



    def save(self):
        user = self.exist()
        if len(user) == 0:

            my_db.insert(f"""INSERT INTO Patient (SSN, username, RegistrationID, FirstName, LastName, age, gender, Race, Occupation, Address, 
                                   Phone, MedicalHistory) VALUES \
                                                                ("{self.ssn}","{self.reg_id}", "{self.reg_id}", "{self.fname.get().strip()}","{self.lname.get().strip()}", "{self.age.get()}", \
                                                                 "{self.gender.get()}", "{self.race.get()}", "{self.job.get().strip()}", "{self.address.get().strip()}", "{self.phone.get()}","{self.history.get().strip()}" );""")
        else:
            user = user[0]
            my_db.insert(f"""Update Patient 
            SET SSN = "{self.ssn}", 
            username = "{self.reg_id}", 
            FirstName = "{self.fname.get()}", LastName = "{self.lname.get()}", 
            age = "{self.age.get()}" , gender = "{self.gender.get()}" , race = "{self.race.get()}",
            Occupation = "{self.job.get()}", Address = "{self.address.get()}", 
            Phone = "{self.phone.get()}", MedicalHistory ="{self.history.get()}" 
            where  
            RegistrationID = "{self.reg_id}";""")

        self.inner_frame.destroy()
        # self.show()

    def show(self):

        inner_frame = tk.LabelFrame(self.master)
        inner_frame.pack(padx=10, pady=10)
        user = [" " for i in range(12)]

        ttk.Button(inner_frame, text='Register', width=18, command = lambda: self.enter_info(user)).grid(row=4, column=0)  # command=self.login
        ttk.Button(inner_frame, text='Update Information', width=18, command = lambda: self.update_info() ).grid(row=5, column=0) #command=self.signup
        ttk.Button(inner_frame, text='Schedule Appointment', width=18).grid(row=6, column=0)  #command=self.signup
        ttk.Button(inner_frame, text='Cancel Appointment', width=18).grid(row=7, column=0) # command=self.signup
        ttk.Button(inner_frame, text='View Information', width=18).grid(row=7, column=0)
        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def update_info(self):

        user = self.exist()
        print(user)
        if len(user) > 0:
            user = user[0]
        else:
            user = [" " for i in range(12)]
        self.enter_info(user = user)

    def exist(self):
        user = my_db.show(f""" SELECT * FROM Patient WHERE username ="{self.reg_id}" or RegistrationID = "{self.reg_id}" """)
        print(my_db.show(f""" SELECT * FROM Patient"""))
        return user

