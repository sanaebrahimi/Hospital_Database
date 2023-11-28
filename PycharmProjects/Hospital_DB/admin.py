from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox
import bcrypt
import hospitallogic
from hospitallogic import User
import dataaccess as da
from nurse import Nurse
my_db = da.DataBaseManagement('three_layered_db.db')

class Admin():
    def __init__(self, master: themed_tk.ThemedTk, password):
        self.master = master
        self.master.title('Admin Homepage')
        self.email_admin = "admin2023@uic.edu"
        self.password = password
        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()
        self.inner_frame = tk.LabelFrame(self.frame)
        self.inner_frame.grid(row=0, column=0)

        user = [" " for i in range(12)]
        ttk.Button(self.inner_frame, text='Register Nurse', width=18, command= lambda: self.register_nurse(user)).grid(row=4, column=0)
        ttk.Button(self.inner_frame, text='Delete Nurse', width=18, command = lambda: self.delete_nurse()).grid(row=5, column=0)
        ttk.Button(self.inner_frame, text='Edit Nurse Info', width=18, command = lambda: self.update_info()).grid(row=6, column=0)
        ttk.Button(self.inner_frame, text='Add Vaccine', width=18, command = lambda: self.add_vaccine([" ", " ", " ", " "])).grid(row=4, column=1)
        ttk.Button(self.inner_frame, text='Update Vaccine', width=18, command = lambda: self.update_vaccine()).grid(row=7, column=1)
        ttk.Button(self.inner_frame, text='View Patient', width=18, command = lambda: self.view_patients()).grid(row=5, column=1)
        ttk.Button(self.inner_frame, text='View Nurse', width=18, command = lambda: self.view_nurses()).grid(row=6, column=1)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)
        
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)



    def register_nurse(self, user):
        # username, FirstName, LastName, Address, Phone, age, gender
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)

        self.fname = tk.StringVar()
        ttk.Label(self.lower_frame, text='First Name').grid(row=0, column=0, sticky='w')
        box1 = ttk.Entry(self.lower_frame, textvariable=self.fname)
        box1.grid(row=1, column=0)
        box1.insert(0,user[2])

        self.lname = tk.StringVar()
        ttk.Label(self.lower_frame, text='Last Name').grid(row=2, column=0, sticky='w')
        box2 = ttk.Entry(self.lower_frame, textvariable=self.lname)
        box2.grid(row=3, column=0)
        box2.insert(0,user[3])

        self.address = tk.StringVar()
        ttk.Label(self.lower_frame, text='Address').grid(row=6, column=0, sticky='w')
        box4 = ttk.Entry(self.lower_frame, textvariable=self.address)
        box4.grid(row=7, column=0)
        box4.insert(0,user[4])

        self.age = tk.StringVar()
        ttk.Label(self.lower_frame, text='Age').grid(row=8, column=0, sticky='w')
        box5 = ttk.Entry(self.lower_frame, textvariable=self.age)
        box5.grid(row=9, column=0)
        box5.insert(0,user[6])

        self.gender = tk.StringVar()
        ttk.Label(self.lower_frame, text="Gender").grid(row=10, column=0, sticky='w')
        box6 = ttk.Combobox(self.lower_frame, state="readonly", values=[" ", "Male", "Female"], textvariable=self.gender)
        box6.grid(row=11, column=0)
        curr = [" ", "Male", "Female"].index(user[7])
        box6.current(curr)

        self.phone = tk.StringVar()
        ttk.Label(self.lower_frame, text="Phone Number").grid(row=12, column=0, sticky='w')
        box7 = ttk.Entry(self.lower_frame, textvariable=self.phone)
        box7.grid(row=13, column=0)
        box7.insert(0,user[5])

        self.email = tk.StringVar()
        ttk.Label(self.lower_frame, text='Email').grid(row=14, column=0, sticky='w')
        box3 = ttk.Entry(self.lower_frame, textvariable=self.email)
        box3.grid(row=15, column=0)
        box3.insert(0,user[1])

        self.password = tk.StringVar()
        ttk.Label(self.lower_frame, text='Password').grid(row=16, column=0, sticky='w')
        box3 = ttk.Entry(self.lower_frame, textvariable=self.password)
        box3.grid(row=17, column=0)
        box3.insert(0,user[-1])

        ttk.Button(self.lower_frame, text='Save', width=18, command = lambda: self.save(Nurse(self.master, user[1]))).grid(row=18, column=0)

        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def save(self, user):
        fields = [self.email.get().strip(), self.fname.get().strip(), self.lname.get().strip(), self.address.get().strip(),
                  self.phone.get(), self.age.get(), self.gender.get(), self.password.get().strip()]
        for field in fields:
            if(field == ""):
                messagebox.showerror(message="Please enter all fields!")
                return

        user = user.exist()
        if len(user) == 0:
            User(fields[0], fields[7], "Nurse").insert()
            my_db.insert(f"""INSERT INTO Nurse(username,FirstName, LastName, Address, Phone, age, gender) 
                         VALUES("{fields[0]}", "{fields[1]}","{fields[2]}",
                         "{fields[3]}", "{fields[4]}","{fields[5]}", "{fields[6]}" );""")
        else:
            my_db.insert(f"""Update Nurse 
                        SET username = "{fields[0]}", FirstName = "{fields[1]}", LastName = "{fields[2]}",
                        Address = "{fields[3]}", Phone = "{fields[4]}", age = "{fields[5]}", gender = "{fields[6]}"
                        WHERE EmployeeID = "{user[0][0]}"; """)
        self.lower_frame.destroy()

    def update_info(self):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        email = tk.StringVar()
        ttk.Label(self.lower_frame, text="Employee Email").grid(row=0, column=0, sticky='w')
        ttk.Entry(self.lower_frame, textvariable=email)

        ttk.Button(self.lower_frame, text='Search', width=18, command = lambda: self.search(Nurse(self.master, email.get()))).grid(row=1, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def search(self, user):
        user = user.exist()
        if len(user) > 0:
            password = my_db.show(f"""SELECT password FROM LogIn WHERE email_address={user[1]} """)[0][0]
            self.register_nurse(user[0] + password)
        else:
            messagebox.showerror(message="No employees match that email!")

    def view_nurses(self):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        nurses = my_db.show("SELECT * from Nurse")
        for i in range(len(nurses)):
            text = str(nurses[i][0]) + "- " + nurses[i][2] + " " + nurses[i][3]
            ttk.Button(self.lower_frame, text=text, width=18, command= lambda i=i: self.view_nurse_schedules(nurses[i])).grid(row=i, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def view_nurse_schedules(self, nurse):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        nurse_schedule = my_db.show(f""" SELECT * from NurseSchedule Where EmployeeID = {nurse[0]}""")
        ttk.Label(self.lower_frame, text=nurse[2] + " " + nurse[3]).grid(row=0, column=0, sticky='w')
        ttk.Label(self.lower_frame, text=nurse[1]).grid(row=0, column=1, sticky='w')
        ttk.Label(self.lower_frame, text= "Schedule: ").grid(row=1, column=0, sticky='w')
        r = 2
        if len(nurse_schedule) > 0:
            for time_schedule in nurse_schedule:
                ttk.Label(self.lower_frame, text= time_schedule[3] + " " + time_schedule[4]).grid(row=r, column=0, sticky='w')
                r += 1
        ttk.Button(self.lower_frame, text="Back", width=18, command=lambda : self.lower_frame.destroy()).grid(row=r+1, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def delete_nurse(self):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        nurses = my_db.show("SELECT * from Nurse")
        r = 2
        for i in range(len(nurses)):
            text = str(nurses[i][0]) + "-" + " " + nurses[i][2] + " " + nurses[i][3]
            ttk.Button(self.lower_frame, text=text, width=18, command=lambda i=i: self.delete_employee(nurses[i])).grid(row=r, column=0)
            r += 1
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def delete_employee(self, employee):
        my_db.show(f""" Delete from Nurse WHERE EmployeeID = "{employee[0]}" and username = "{employee[1]}" """)
        my_db.show(f""" Delete from NurseSchedule WHERE EmployeeID = "{employee[0]}" and email = "{employee[0]}" """)
        self.delete_nurse()

    def view_patients(self):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        patients = my_db.show(f"""SELECT * from Patient""")
        for i in range(len(patients)):
            text = str(patients[i][1]) + "- " + patients[i][3] + " " + patients[i][4]
            ttk.Button(self.lower_frame, text=text, width=18,
                       command = lambda i=i: self.view_patients_schedules(patients[i])).grid(row=i, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def view_patients_schedules(self, patient):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        patient_schedule = my_db.show(f"""SELECT * from VaccineSchedule Where registration_id = "{patient[1]}" """)
        ttk.Label(self.lower_frame, text=patient[2] + " " + patient[3]).grid(row=0, column=0, sticky='w')
        ttk.Label(self.lower_frame, text=patient[1]).grid(row=0, column=1, sticky='w')
        ttk.Label(self.lower_frame, text= "Schedule: ").grid(row=1, column=0, sticky='w')
        r = 2
        if len(patient_schedule) > 0:
            for time_schedule in patient_schedule:
                text = "Vaccine: " +  time_schedule[5] + "- Date & Time: " + time_schedule[6] + " " + time_schedule[7]
                ttk.Label(self.lower_frame, text=text).grid(row=r, column=0, sticky='w')
                r += 1
        ttk.Button(self.lower_frame, text="Back",
                   width=18, command=lambda : self.lower_frame.destroy()).grid(row=r+1, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def add_vaccine(self, vacc):
        # VaccName, Available_Dose, OnHold_Dose
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)

        self.vax_name = tk.StringVar()
        ttk.Label(self.lower_frame, text='Vaccine Name').grid(row=0, column=0, sticky='w')
        box5 = ttk.Entry(self.lower_frame, textvariable=self.vax_name)
        box5.grid(row=1, column=0)
        box5.insert(0, vacc[0])

        self.vax_available_dose = tk.StringVar()
        ttk.Label(self.lower_frame, text='Vaccine Available dose').grid(row=0, column=1, sticky='w')
        box5 = ttk.Entry(self.lower_frame, textvariable=self.vax_available_dose)
        box5.grid(row=1, column=1)
        box5.insert(0, vacc[1])

        self.vax_onhold = tk.StringVar()
        ttk.Label(self.lower_frame, text='Vaccine OnHold dose').grid(row=0, column=2, sticky='w')
        box6 = ttk.Entry(self.lower_frame, textvariable=self.vax_onhold)
        box6.grid(row= 1, column=2)
        box6.insert(0, vacc[2])

        self.company_name= tk.StringVar()
        ttk.Label(self.lower_frame, text='Company').grid(row=0, column=3, sticky='w')
        box7 = ttk.Entry(self.lower_frame, textvariable=self.company_name)
        box7.grid(row=1, column=3)
        box7.insert(0, vacc[3])

        ttk.Button(self.lower_frame, text="Save",
                   width=18, command=lambda: self.save_vaccine()).grid(row=2, column=0)
        for widget in self.lower_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def save_vaccine(self):
        fields = [self.vax_name.get().strip(), self.vax_available_dose.get().strip(),
                  self.vax_onhold.get().strip(), self.company_name.get().strip()]
        for field in fields:
            if(field == ""):
                messagebox.showerror(message="Please enter all fields!")
                return
        selection = my_db.show(f"""SELECT * from Vaccine where VaccName = "{fields[0]}" """)
        if len(selection) > 0:
            my_db.insert(f"""Update Vaccine
                            SET 
                            Available_Dose = Available_Dose + "{fields[1]}" , 
                            OnHold_Dose = OnHold_Dose + "{fields[2]}"  
                            where  
                            VaccName = "{fields[0]}"; """)
        else:
            my_db.insert(f""" INSERT INTO Vaccine(VaccName, Available_Dose, OnHold_Dose, CompanyName)
                         VALUES("{fields[0]}", "{fields[1]}", "{fields[2]}", "{fields[3]}") """)
        self.lower_frame.destroy()

    def update_vaccine(self):
        self.lower_frame.destroy()
        self.lower_frame = tk.LabelFrame(self.frame)
        self.lower_frame.grid(row=1, column=0)
        vaccines = my_db.show("SELECT * from Vaccine")
        if len(vaccines) > 0:
            tk.Label(self.lower_frame, text="Vaccines", font=("Arial", 30)).grid(row=0, columnspan=3)
            # create Treeview with 3 columns
            cols = ('Name', 'Available Dose', 'Dose OnHold', 'Company')
            tree = ttk.Treeview(self.lower_frame, columns=cols, show='headings')

            # set column headings
            for col in cols:
                tree.heading(col, text=col)
            tree.grid(row=1, column=0, columnspan=2)
            for vaccine in vaccines:
                tree.insert("", "end", values=vaccine)

            def _element(event):
                tree = event.widget
                for item in tree.selection():
                    print(tree.item(item))
                    values = tree.item(item)["values"]
                    tk.Button(self.lower_frame, text="Update", width=15,
                            command=lambda: self.add_vaccine(values)).grid(row=4, column=0)

            tree.bind("<<TreeviewSelect>>", _element)

            for widget in self.lower_frame.children.values():
                widget.grid_configure(padx=50, pady=5)

