from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox
import bcrypt
import hospitallogic
from hospitallogic import User
import dataaccess as da
from tkcalendar import Calendar
from datetime import date
from datetime import datetime
my_db = da.DataBaseManagement('three_layered_db.db')

class Patient():
    def __init__(self, master: themed_tk.ThemedTk, email):
        self.master = master
        self.master.title('Patient Homepage')
        self.reg_id = email
        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()






    def enter_info(self, user, update=False):
        if not update and len(self.exist()) > 0:
            messagebox.showerror(message="Already registered!")
            return

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
        box5 = ttk.Combobox(self.inner_frame, state="readonly", values=[" ", "Male", "Female"], textvariable=self.gender)
        box5.grid(row=9, column=0)
        curr = [" ","Male", "Female"].index(user[6])
        box5.current(curr)

        self.race = tk.StringVar()
        ttk.Label(self.inner_frame, text="Race").grid(row=8, column=1, sticky='w')
        box6 = ttk.Combobox(self.inner_frame, state="readonly", values=[" ","Hispanic", "African American", "White"], textvariable=self.race)
        box6.grid(row=9, column=1)
        curr = [" ","Hispanic", "African American", "White"].index(user[7])
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
                                                                ("{self.ssn.get()}","{self.reg_id}", "{self.reg_id}", "{self.fname.get().strip()}","{self.lname.get().strip()}", "{self.age.get()}", \
                                                                 "{self.gender.get()}", "{self.race.get()}", "{self.job.get().strip()}", "{self.address.get().strip()}", "{self.phone.get()}","{self.history.get().strip()}" );""")
        else:
            user = user[0]
            my_db.insert(f"""Update Patient 
            SET SSN = "{self.ssn.get()}", 
            username = "{self.reg_id}", 
            FirstName = "{self.fname.get()}", LastName = "{self.lname.get()}", 
            age = "{self.age.get()}" , gender = "{self.gender.get()}" , race = "{self.race.get()}",
            Occupation = "{self.job.get()}", Address = "{self.address.get()}", 
            Phone = "{self.phone.get()}", MedicalHistory ="{self.history.get()}" 
            where  
            RegistrationID = "{self.reg_id}";""")

        self.inner_frame.destroy()
        return
        # self.show()

    def show(self):

        inner_frame = tk.LabelFrame(self.master)
        inner_frame.pack(padx=10, pady=10)
        user = [" " for i in range(12)]
        record_check = my_db.show(f"""SELECT * from VaccineRecord WHERE registration_id = "{self.reg_id}" """)
        if len(record_check) > 0:
            record = record_check
            ttk.Button(inner_frame, text='Vaccination Record', width=18, command=lambda: self.view_record(record)).grid(row=9,
                                                                                                                  column=0)
        ttk.Button(inner_frame, text='Register', width=18, command = lambda: self.enter_info(user)).grid(row=4, column=0)  # command=self.login
        ttk.Button(inner_frame, text='Update Information', width=18, command = lambda: self.update_info(user)).grid(row=5, column=0) #command=self.signup
        ttk.Button(inner_frame, text='Schedule Appointment', width=18, command = lambda: self.scheduling()).grid(row=6, column=0)  #command=self.signup
        ttk.Button(inner_frame, text='Cancel Appointment', width=18, command= lambda: self.cancel_appointment()).grid(row=7, column=0) # command=self.signup
        ttk.Button(inner_frame, text='View Information', width=18, command = lambda: self.view_schedule()).grid(row=8, column=0)
        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def update_info(self, user):

        user_exists = self.exist()
        if len(user_exists) > 0:
            user = user_exists.pop()
        self.enter_info(user = user, update=True)


    def select_nurse(self, details, vaccine):

        number_check = my_db.show(f"""Select numberof_patients_per_nurse from NurseSchedule where id = {details[4]}""").pop()[0]
        vaccine_availability = my_db.show(f"""Select Available_Dose from Vaccine where VaccName = "{vaccine}" """)
        if len(vaccine_availability) ==0:
            messagebox.showerror(message="Your selected Vaccine is not available!")
            return
        vaccine_availability = vaccine_availability.pop()[0]
        if number_check < 12 and vaccine_availability > 0:
            my_db.insert(
                f""" INSERT INTO VaccineSchedule(schedule_id, registration_id, vaccine_name, NursePractioner, date, time)VALUES \
                ("{details[4]}","{self.reg_id}", "{vaccine}", "{details[1]}", "{details[2]}", "{details[3]}") """)
            my_db.insert(f"""Update NurseSchedule
                            SET 
                            numberof_patients_per_nurse = numberof_patients_per_nurse + 1
                            WHERE 
                            id = {details[4]} """)
            my_db.insert(f"""Update Vaccine
                                        SET 
                                        OnHold_Dose = OnHold_Dose + 1
                                        WHERE 
                                        VaccName = "{vaccine}" """)
        elif vaccine_availability  == 0 :
            messagebox.showerror(message="Your selected Vaccine is not available!")
            return
        elif number_check == 12 :
            messagebox.showerror(message="Your selected Nurse is not available!")
            return
        print(my_db.show(f"""select * from VaccineSchedule"""))
        print(my_db.show(f"""select * from NurseSchedule"""))
        self.inner_frame.destroy()
        return

    def scheduling(self):
        available_dates = my_db.show(f""" select * from NurseSchedule""")
        print(available_dates)
        if len(available_dates) == 0:
            messagebox.showerror(message="No availability!")
            return
        nurses = []
        date_times = []
        date_time_nurse = {}
        options = tuple()
        for dt in available_dates:
            date_time = dt[3] + " " + dt[4]
            date_times.append(date_time)
            name = my_db.show(
                f""" SELECT FirstName, LastName from Nurse WHERE EmployeeID = {dt[1]} """)
            name = name[0][0] + " " + name[0][1]
            nurses.append(name)
            tmp =  date_time + "-"+ "Nurse: "+ name
            date_time_nurse[tmp] = [name, dt[1], dt[3], dt[4], dt[0]]
            options += (tmp,)


        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        dt_nurse = tk.StringVar()

        selected_dt = ttk.OptionMenu(self.inner_frame, dt_nurse,*options)
        selected_dt.config(width=25)
        selected_dt.pack(pady=20, padx=20)
        choice = date_time_nurse[dt_nurse.get()]

        vaccine = tk.StringVar()
        vax = ('Pfizer', 'Moderna', 'J&J')
        selected_vax = ttk.OptionMenu(self.inner_frame, vaccine, *vax)
        selected_vax.config(width=25)
        selected_vax.pack(pady=20, padx=20)

        b1 = ttk.Button(self.inner_frame, text="Select", command=lambda: self.select_nurse(choice, vaccine.get())) #command=grad_date()
        b1.pack(pady=20)


    def view_schedule(self):

        patient_schedule = my_db.show(f""" SELECT * from VaccineSchedule Where registration_id = "{self.reg_id}" """)

        patient = self.exist()
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        if len(patient) > 0:
            patient = patient[0]
        ttk.Label(self.inner_frame, text=patient[3] + " " + patient[4]).grid(row=1, column=0, sticky='w')
        ttk.Label(self.inner_frame, text=patient[2]).grid(row=1, column=1, sticky='w')
        ttk.Label(self.inner_frame, text="Schedule: ").grid(row=2, column=0, sticky='w')
        r = 4
        if len(patient_schedule) == 0:
            messagebox.showerror(message="Nothing scheduled yet!")
        else:
            for time_schedule in patient_schedule:
                ttk.Label(self.inner_frame, text=time_schedule[6] + " " + time_schedule[7] + "- Vaccine: " + time_schedule[5]).grid(row=r, column=0,                                                                                             sticky='w')
                r += 1
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)
        return

    def view_record(self, records):

        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)

        tk.Label(self.inner_frame, text="Vaccine Record", font=("Arial", 30)).grid(row=0, columnspan=3)

        cols = ('ID', 'First Name', 'Last Name', 'Vaccine Name', 'Date', 'Time','Nurse')
        tree = ttk.Treeview(self.inner_frame, columns=cols, show='headings')

        for col in cols:
            tree.heading(col, text=col)
        for record in records:
            fname, lname = my_db.show(
                f"""SELECT FirstName, LastName from Patient WHERE RegistrationID = "{record[2]}" """).pop()
            fnurse, lnurse = my_db.show(f"SELECT FirstName, LastName from Nurse WHERE EmployeeID = {record[4]}").pop()
            tree.grid(row=1, column=0, columnspan=2)
            vax = (record[0], fname, lname, record[3], record[5], record[6], fnurse+ " " + lnurse)
            tree.insert("", "end", values=vax)


        tk.Button(self.inner_frame, text="Back", width=15,
                          command=lambda: self.inner_frame.destroy()).grid(row=4, column=0)


        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def delete_appointment(self, info):
        print(my_db.show(f"""select * from NurseSchedule"""))
        print(my_db.show(f"""select * from Vaccine"""))
        my_db.insert(f"""DELETE from VaccineSchedule WHERE appointment_id = {info[0]}""")
        my_db.insert(f"""UPDATE Vaccine
                        SET OnHold_Dose = OnHold_Dose-1,
                            Available_Dose = Available_Dose+1 
                        WHERE VaccName = "{info[2]}" """)
        my_db.insert(f"""UPDATE NurseSchedule
                                SET numberof_patients_per_nurse = numberof_patients_per_nurse-1
                                WHERE id= {info[1]}""")
        print(my_db.show(f"""select * from NurseSchedule"""))
        print(my_db.show(f"""select * from Vaccine"""))
        self.inner_frame.destroy()
        return
    def cancel_appointment(self):
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        appointments = my_db.show(f"""SELECT * from VaccineSchedule WHERE registration_id = "{self.reg_id}" AND vax_status ="F" """)
        print(appointments)
        if len(appointments) == 0:
            messagebox.showerror(message="Nothing to Cancel!")
            return
        tk.Label(self.inner_frame, text="Appointment", font=("Arial", 30)).grid(row=0, columnspan=3)

        cols = ('ID', 'Schedule ID','Vaccine Name', 'Date', 'Time')
        tree = ttk.Treeview(self.inner_frame, columns=cols, show='headings')

        for col in cols:
            tree.heading(col, text=col)
        for record in appointments:
            tree.grid(row=1, column=0, columnspan=2)
            vax = (record[0], record[2], record[5], record[6], record[7])
            tree.insert("", "end", values=vax)

        def _element(event):
            tree = event.widget
            for item in tree.selection():
                print(tree.item(item))
                values = tree.item(item)["values"]
                tk.Button(self.inner_frame, text="Cancel Appointment", width=15,
                          command=lambda: self.delete_appointment(values)).grid(row=4, column=0)

        tree.bind("<<TreeviewSelect>>", _element)
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def exist(self):
        user = my_db.show(f""" SELECT * FROM Patient WHERE username ="{self.reg_id}" or RegistrationID = "{self.reg_id}" """)
        print(my_db.show(f""" SELECT * FROM Patient"""))
        return user


