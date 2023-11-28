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


    def show(self):
        nurse = self.exist()
        if len(nurse) == 0:
            return None
        nurse = nurse.pop()
        self.inner_frame = tk.LabelFrame(self.frame)
        self.inner_frame.grid(row=0, column=0)

        ttk.Label(self.inner_frame, text=nurse[2] + " " + nurse[3]).grid(row=0, column=0)
        ttk.Label(self.inner_frame, text=nurse[4]).grid(row=1, column=0)
        ttk.Label(self.inner_frame, text=nurse[5]).grid(row=2, column=0)
        ttk.Label(self.inner_frame, text=str(nurse[7]) +" "+ str(nurse[6])).grid(row=3, column=0)

        ttk.Button(self.inner_frame, text='Edit Info', width=18, command=lambda: self.enter_info(nurse[0])).grid(row=4, column=0)
        ttk.Button(self.inner_frame, text='Schedule Timeslot', width=18, command=lambda: self.scheduling(nurse[0])).grid(row=5, column=0)
        ttk.Button(self.inner_frame, text='Cancel Timeslot', width=18, command=lambda: self.cancel_timeslots(nurse[0])).grid(row=6, column=0)
        ttk.Button(self.inner_frame, text='View Timeslots', width=18, command=lambda: self.view_timeslots(nurse[0])).grid(row=7, column=0)
        ttk.Button(self.inner_frame, text='View Patients', width=18,
                   command=lambda: self.view_patients_perslot(nurse[0])).grid(row=8, column=0)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)
        
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)

    def enter_info(self, emp_id):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        nurse_info = my_db.show(f"""select Phone, Address from Nurse WHERE EmployeeID ={emp_id}""").pop()
        self.address = tk.StringVar()
        ttk.Label(self.lower_frame, text='Address').grid(row=0, column=0, sticky='w')
        box1= ttk.Entry(self.lower_frame, textvariable=self.address)
        box1.grid(row=1, column=0)
        box1.insert(0, nurse_info[1])

        self.phone = tk.StringVar()
        ttk.Label(self.lower_frame, text="Phone Number").grid(row=2, column=0, sticky='w')
        box2 = ttk.Entry(self.lower_frame, textvariable=self.phone)
        box2.grid(row=3, column=0)
        box2.insert(0, nurse_info[0])

        ttk.Button(self.lower_frame, text='Save', width=18, command = lambda: self.save()).grid(row=4, column=0)

        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def save(self):
        user = self.exist()
        user = user[0]
        fields = [self.address.get().strip(), self.phone.get().strip()]
        if(fields[0] != "" and fields[1] != ""):
            my_db.insert(f"""Update Nurse 
                SET 
                Address = "{fields[0]}", 
                Phone = "{fields[1]}"
                where  
                EmployeeID  = "{user[0]}";""")
            self.lower_frame.destroy()
            self.inner_frame.destroy()
            self.show()
        else:
            messagebox.showerror(message="Please enter all fields!")

    def scheduling(self, employee_id):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        time = tk.StringVar()
        options = ("10-11 AM", "11-12 PM", "12-1 PM", "1-2 PM", "2-3 PM", "3-4 PM")
        todays_date = date.today()
        slot = ttk.OptionMenu(self.lower_frame, time,*options)
        slot.config(width=25)
        slot.pack(pady=20, padx=20)
        cal = Calendar(self.lower_frame,  background="black", bordercolor="black",
               headersbackground="white", normalbackground="white", foreground='black',
               normalforeground='black', headersforeground='black', selectmode='day',
                year=todays_date.year, month=todays_date.month, day=todays_date.day)

        cal.pack(pady=20, padx=20)
        b1 = ttk.Button(self.lower_frame, text="Submit", command=lambda: self.on_click(cal.get_date(), time.get(), employee_id))
        b1.pack(pady=20)

        date1 = ttk.Label(self.lower_frame, text="")
        date1.pack(pady=20)

    def on_click(self, date, time_slot,user):
        my_db.insert(f""" INSERT INTO NurseSchedule(EmployeeID, email, date, time)
                     VALUES ("{user}", "{self.email}", "{date}", "{time_slot}") """)
        self.lower_frame.destroy()
        self.inner_frame.destroy()
        self.show()

    def view_timeslots(self, employee_id):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        timeslots = my_db.show(f"""SELECT * from NurseSchedule WHERE EmployeeID = {employee_id} """)
        for i in range(len(timeslots)):
            text = "View " + str(timeslots[i][3]) + " - " + str(timeslots[i][4])
            ttk.Button(self.lower_frame, text=text, width=25,
                       command = lambda i=i: self.view_timeslot(timeslots[i])).grid(row=i, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def view_timeslot(self, timeslot):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        ttk.Label(self.lower_frame, text=timeslot[3] + " " + timeslot[4]).grid(row=0, column=0, sticky='w')
        ttk.Label(self.lower_frame, text=timeslot[5]).grid(row=0, column=1, sticky='w')
        ttk.Button(self.lower_frame, text="Back", width=18, command=lambda : self.view_timeslots(timeslot[1])).grid(row=1, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def cancel_timeslots(self, employee_id):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        timeslots = my_db.show(f"""SELECT * from NurseSchedule WHERE EmployeeID = {employee_id} """)
        for i in range(len(timeslots)):
            text = "Cancel " + str(timeslots[i][3]) + " - " + str(timeslots[i][4])
            print(timeslots[i])
            ttk.Button(self.lower_frame, text=text, width=22,
                       command = lambda i=i: self.cancel_timeslot(timeslots[i][0])).grid(row=i, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)
    
    def cancel_timeslot(self, timeslot):
        print(my_db.show(f"""select * from NurseSchedule """))
        my_db.insert(f""" Delete from NurseSchedule WHERE id = "{timeslot}" """)
        print(my_db.show(f"""select * from NurseSchedule """))
        self.lower_frame.destroy()
        return

        # self.cancel_timeslots()
    def change_patient_status(self, patient):
        print(my_db.show(f"""SELECT * from Vaccine"""))
        my_db.insert(f"""Update VaccineSchedule 
                        SET 
                        vax_status = "T"
                        where  
                        appointment_id  = "{patient[0]}";""")
        print(my_db.show(f"""SELECT * from Vaccine"""))
        return
    def view_patients_perslot(self, emp_id):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        vaccines = my_db.show(f"SELECT * from VaccineSchedule WHERE NursePractioner = {emp_id}")
        print(my_db.show(f"""SELECT * from VaccineRecord"""))
        if len(vaccines) > 0:
            tk.Label(self.lower_frame, text="Patients", font=("Arial", 30)).grid(row=0, columnspan=3)
            # create Treeview with 3 columns
            cols = ('ID','First Name', 'Last Name', 'Age', 'Vaccine Name', 'Date', 'Time', 'Status')
            tree = ttk.Treeview(self.lower_frame, columns=cols, show='headings')

            # set column headings
            for col in cols:
                tree.heading(col, text=col)
            tree.grid(row=1, column=0, columnspan=2)
            for vaccine in vaccines:
                fname, lname, age = my_db.show(f"""SELECT FirstName, LastName, age from Patient WHERE RegistrationID = "{vaccine[3]}" """ ).pop()
                vax = (vaccine[0], fname,lname,age, vaccine[5], vaccine[6], vaccine[7], vaccine[1])
                tree.insert("", "end", values=vax)

            def _element(event):
                tree = event.widget
                for item in tree.selection():
                    print(tree.item(item))
                    values = tree.item(item)["values"]
                    tk.Button(self.lower_frame, text="Change Status", width=15,
                              command=lambda: self.change_patient_status(values)).grid(row=4, column=0)

            tree.bind("<<TreeviewSelect>>", _element)

            for widget in self.lower_frame.children.values():
                widget.grid_configure(padx=50, pady=5)


    def exist(self):
        user = my_db.show(f""" SELECT * FROM Nurse WHERE username ="{self.email}" """)
        return user


