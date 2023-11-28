from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import *
from tkcalendar import Calendar
from datetime import date
from datetime import datetime
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
        user = self.exist()
        user = user[0]
        my_db.insert(f"""Update Patient 
            SET 
            Address = "{self.address.get()}", 
            Phone = "{self.phone.get()}"
            where  
            EmployeeID  = "{user[0]}";""")

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
        ttk.Button(inner_frame, text='Schedule Appointment', width=18, command=lambda: self.scheduling(nurse[0])).grid(row=5, column=0) #command=self.signup
        ttk.Button(inner_frame, text='Cancel Appointment', width=18).grid(row=6, column=0)  #command=self.signup
        ttk.Button(inner_frame, text='View Schedule', width=18).grid(row=7, column=0) # command=self.signup

        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

        self.frame.destroy()
        return

    def on_click(self, date, time_slot,user):
        count = my_db.show(f"""SELECT COUNT(schedule_id) from Hospital WHERE date = "{date}"  AND time = "{time_slot}" """)
        my_db.insert(f""" INSERT INTO NurseSchedule(EmployeeID, email, date, time)VALUES ("{user}", "{self.email}", "{date}", "{time_slot}") """)
        if count[0][0] == 0:
            my_db.insert(f"""INSERT INTO Hospital (date, time) VALUES ("{date}", "{time_slot}")""")

        self.inner_frame.destroy()
        return

    def scheduling(self, employee_id):
        print(my_db.show(f""" select * from Hospital"""))
        print(my_db.show(f""" select * from NurseSchedule"""))
        print(my_db.show(f"""SELECT COUNT(EmployeeID) from NurseSchedule GROUP BY date, time"""))

        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        time = tk.StringVar()
        options = ("10-11 AM", "11-12 PM", "12-1 PM", "1-2 PM", "2-3 PM", "3-4 PM")
        todays_date = date.today()
        slot = ttk.OptionMenu(self.inner_frame, time,*options)
        slot.config(width=25)
        slot.pack(pady=20, padx=20)
        cal = Calendar(self.inner_frame,  background="black", bordercolor="black",
               headersbackground="white", normalbackground="white", foreground='black',
               normalforeground='black', headersforeground='black', selectmode='day',
                year=todays_date.year, month=todays_date.month, day=todays_date.day)

        cal.config(background="black")
        cal.pack(pady=20, padx=20)
        b1 = ttk.Button(self.inner_frame, text="Submit", command=lambda: self.on_click(cal.get_date(), time.get(), employee_id)) #command=grad_date()
        b1.pack(pady=20)

        date1 = ttk.Label(self.inner_frame, text="")
        date1.pack(pady=20)


    def exist(self, email = None):
        user = my_db.show(f""" SELECT * FROM Nurse WHERE username ="{self.email}" """)
        return user


