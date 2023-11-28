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
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)

        user = [" " for i in range(12)]
        ttk.Button(self.inner_frame, text='Register Employee', width=18, command= lambda: self.register_nurse(user)).grid(row=4, column=0)  # command=self.login
        ttk.Button(self.inner_frame, text='Delete Employee', width=18, command = lambda: self.delete_nurse()).grid(row=5, column=0)
        ttk.Button(self.inner_frame, text='Edit Employee Information', width=18, command = lambda: self.update_info()).grid(row=6, column=0)
        ttk.Button(self.inner_frame, text='Add Vaccine', width=18, command = lambda: self.add_vaccine([" ", " ", " ", " "])).grid(row=4, column=1)  # command=self.signup
        ttk.Button(self.inner_frame, text='Update Vaccine', width=18, command = lambda: self.update_vaccine()).grid(row=7, column=1)  # command=self.signup
        ttk.Button(self.inner_frame, text='View Patient', width=18, command = lambda: self.view_patients()).grid(row=5, column=1)  # command=self.signup
        ttk.Button(self.inner_frame, text='View Nurse', width=18, command = lambda: self.view_nurses()).grid(row=6, column=1)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)



    def register_nurse(self, user):
        # username, FirstName, LastName, Address, Phone, age, gender

        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)

        self.fname = tk.StringVar()
        ttk.Label(self.inner_frame, text='First Name').grid(row=0, column=0, sticky='w')
        box1 = ttk.Entry(self.inner_frame, textvariable=self.fname)
        box1.grid(row=1, column=0)
        box1.insert(0,user[2])

        self.lname = tk.StringVar()
        ttk.Label(self.inner_frame, text='Last Name').grid(row=2, column=0, sticky='w')
        box2 = ttk.Entry(self.inner_frame, textvariable=self.lname)
        box2.grid(row=3, column=0)
        box2.insert(0,user[3])

        self.email = tk.StringVar()
        ttk.Label(self.inner_frame, text='Email').grid(row=4, column=0, sticky='w')
        box3 = ttk.Entry(self.inner_frame, textvariable=self.email)
        box3.grid(row=5, column=0)
        box3.insert(0,user[1])

        self.address = tk.StringVar()
        ttk.Label(self.inner_frame, text='Address').grid(row=6, column=0, sticky='w')
        box4 = ttk.Entry(self.inner_frame, textvariable=self.address)
        box4.grid(row=7, column=0)
        box4.insert(0,user[4])

        self.age = tk.StringVar()
        ttk.Label(self.inner_frame, text='Age').grid(row=8, column=0, sticky='w')
        box5 = ttk.Entry(self.inner_frame, textvariable=self.age)
        box5.grid(row=9, column=0)
        box5.insert(0,user[6])

        self.gender = tk.StringVar()
        ttk.Label(self.inner_frame, text="Gender").grid(row=10, column=0, sticky='w')
        box6 = ttk.Combobox(self.inner_frame, state="readonly", values=[" ", "Male", "Female"], textvariable=self.gender)
        box6.grid(row=11, column=0)
        curr = [" ", "Male", "Female"].index(user[7])
        box6.current(curr)

        self.phone = tk.StringVar()
        ttk.Label(self.inner_frame, text="Phone Number").grid(row=12, column=0, sticky='w')
        box7 = ttk.Entry(self.inner_frame, textvariable=self.phone)
        box7.grid(row=13, column=0)
        box7.insert(0,user[5])
        ttk.Button(self.inner_frame, text='Save', width=18, command = lambda: self.save(Nurse(self.master, user[1]))).grid(row=14, column=0)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

        # self.inner_frame.destroy()


    def save(self, user):
        user = user.exist()
        if len(user) == 0:
            my_db.insert(f"""INSERT INTO Nurse(username,FirstName, LastName, Address, Phone, age, gender) VALUES \
                                                                ("{self.email.get().strip()}", "{self.fname.get().strip()}","{self.lname.get().strip()}", "{self.address.get().strip()}",  "{self.phone.get()}","{self.age.get()}", \
                                                                 "{self.gender.get()}" );""")

        else:
            user = user[0]
            my_db.insert(f"""Update Nurse 
                        SET username = "{self.email.get().strip()}", 
                        FirstName = "{self.fname.get().strip()}", LastName = "{self.lname.get().strip()}", 
                        age = "{self.age.get()}" , gender = "{self.gender.get()}" , 
                        Address = "{self.address.get()}", 
                        Phone = "{self.phone.get()}"  
                        where  
                        EmployeeID = "{user[0]}";""")
        self.inner_frame.destroy()
        return
    def update_info(self):

        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        email = tk.StringVar()
        ttk.Label(self.inner_frame, text="Employee Email").grid(row=1, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=email)

        ttk.Button(self.inner_frame, text='Search', width=18, command = lambda: self.search(Nurse(self.master, email.get()))).grid(row=2, column=0)
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

        # self.inner_frame.destroy()
    def search(self, user):
        self.inner_frame.destroy()
        user = user.exist()

        if len(user) > 0:
            user = user[0]

        else:
            user = [" " for i in range(12)]
        self.register_nurse(user=user)

    def view_nurses(self):

        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        nurses = my_db.show(f""" SELECT * from Nurse""")
        print(nurses)
        r = 2
        for i in range(len(nurses)): #nurse in nurses:
            ttk.Button(self.inner_frame, text=str(nurses[i][0])+"-"+" " + nurses[i][2] +" " + nurses[i][3], width=18, command = lambda i=i: self.view_nurse_schedules([nurses[i][0],nurses[i][1], nurses[i][2], nurses[i][3]])).grid(row=r, column=0)
            # ttk.Label(self.inner_frame, text= ).grid(row=r, column=1, sticky='w')
            r += 1
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)



    def view_nurse_schedules(self, nurse):
        self.inner_frame.destroy()

        nurse_schedule = my_db.show(f""" SELECT * from NurseSchedule Where EmployeeID = {nurse[0]}""")
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        print(nurse_schedule[0])
        ttk.Label(self.inner_frame, text=nurse[2] + " " + nurse[3]).grid(row=1, column=0, sticky='w')
        ttk.Label(self.inner_frame, text=nurse[1]).grid(row=1, column=1, sticky='w')
        ttk.Label(self.inner_frame, text= "Schedule: ").grid(row=2, column=0, sticky='w')
        r  = 4
        if len(nurse_schedule) > 0:
            for time_schedule in nurse_schedule:
                ttk.Label(self.inner_frame, text= time_schedule[3] + " " + time_schedule[4] ).grid(row=r, column=0, sticky='w')
                r += 1

        ttk.Button(self.inner_frame, text="Back",
                   width=18, command=lambda : self.inner_frame.destroy()).grid(row=r+1, column=0)
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)


        # self.inner_frame.destroy()



    def delete_nurse(self):
        # self.inner_frame.destroy()
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        nurses = my_db.show(f""" SELECT * from Nurse""")
        r = 2
        for i in range(len(nurses)):  # nurse in nurses:
            ttk.Button(self.inner_frame, text=str(nurses[i][0]) + "-" + " " + nurses[i][2] + " " + nurses[i][3],
                       width=18, command=lambda i=i: self.delete_employee(
                    [nurses[i][0], nurses[i][1], nurses[i][2], nurses[i][3]])).grid(row=r, column=0)
            # ttk.Label(self.inner_frame, text= ).grid(row=r, column=1, sticky='w')
            r += 1
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def delete_employee(self, employee):
        self.inner_frame.destroy()
        my_db.show(f""" Delete from Nurse WHERE EmployeeID = "{employee[0]}" and username = "{employee[1]}" """)
        my_db.show(f""" Delete from NurseSchedule WHERE EmployeeID = "{employee[0]}" and email = "{employee[0]}" """)
        #
        self.delete_nurse()
        self.inner_frame.destroy()
        return

    def view_patients_schedules(self, patient):
        self.inner_frame.destroy()

        patient_schedule = my_db.show(f""" SELECT * from VaccineSchedule Where registration_id = "{patient[1]}" """)
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        print(patient_schedule)

        ttk.Label(self.inner_frame, text=patient[2] + " " + patient[3]).grid(row=1, column=0, sticky='w')
        ttk.Label(self.inner_frame, text=patient[1]).grid(row=1, column=1, sticky='w')
        ttk.Label(self.inner_frame, text= "Schedule: ").grid(row=2, column=0, sticky='w')
        r  = 4
        if len(patient_schedule) > 0:
            for time_schedule in patient_schedule:
                string = "Vaccine: " +  time_schedule[5] + "- Date & Time: " + time_schedule[3] + " " + time_schedule[4]
                ttk.Label(self.inner_frame, text= string ).grid(row=r, column=0, sticky='w')
                r += 1

        ttk.Button(self.inner_frame, text="Back",
                   width=18, command=lambda : self.inner_frame.destroy()).grid(row=r+1, column=0)
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)


    def view_patients(self):

        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        patients = my_db.show(f""" SELECT * from Patient""")
        print(patients)
        r = 2
        for i in range(len(patients)): #nurse in nurses:
            ttk.Button(self.inner_frame, text=str(patients[i][1])+"-"+" " + patients[i][3] +" " + patients[i][4], width=18, command = lambda i=i: self.view_patients_schedules([patients[i][1],patients[i][2], patients[i][3], patients[i][4]])).grid(row=r, column=0)
            r += 1
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)


    def save_vaccine(self):
        query = my_db.show(f"""SELECT * from Vaccine where VaccName = "{self.vax_name.get().strip()}" """)
        if len(query) > 0:
            print(query)
            query = query.pop()
            my_db.insert(f"""Update Vaccine
                                    SET 
                                    Available_Dose = Available_Dose + "{self.vax_available_dose.get()}" , 
                                    OnHold_Dose = OnHold_Dose + "{self.vax_onhold.get()}"  
                                    where  
                                    VaccName = "{self.vax_name.get().strip()}" ;""")

        else:
            my_db.insert(f""" INSERT INTO Vaccine(VaccName, Available_Dose, OnHold_Dose, CompanyName) VALUES\
                            ("{self.vax_name.get().strip()}", "{self.vax_available_dose.get().strip()}", "{self.vax_onhold.get().strip()}", "{self.company_name.get().strip()}")""")

        self.inner_frame.destroy()
        print(my_db.show(f"""SELECT * from Vaccine"""))
        return

    def add_vaccine(self, vacc):
        # VaccName
        # Available_Dose
        # OnHold_Dose
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        # vacc = [" ", " ", " ", " "]

        self.vax_name = tk.StringVar()
        ttk.Label(self.inner_frame, text='Vaccine Name').grid(row=0, column=0, sticky='w')
        box5 = ttk.Entry(self.inner_frame, textvariable=self.vax_name)
        box5.grid(row=1, column=0)
        box5.insert(0, vacc[0])

        self.vax_available_dose = tk.StringVar()
        ttk.Label(self.inner_frame, text='Vaccine Available dose').grid(row=0, column=1, sticky='w')
        box5 = ttk.Entry(self.inner_frame, textvariable=self.vax_available_dose)
        box5.grid(row=1, column=1)
        box5.insert(0, vacc[1])


        self.vax_onhold = tk.StringVar()
        ttk.Label(self.inner_frame, text='Vaccine OnHold dose').grid(row=0, column=2, sticky='w')
        box6 = ttk.Entry(self.inner_frame, textvariable=self.vax_onhold)
        box6.grid(row= 1, column=2)
        box6.insert(0, vacc[2])

        self.company_name= tk.StringVar()
        ttk.Label(self.inner_frame, text='Company').grid(row=0, column=3, sticky='w')
        box7 = ttk.Entry(self.inner_frame, textvariable=self.company_name)
        box7.grid(row=1, column=3)
        box7.insert(0, vacc[3])

        ttk.Button(self.inner_frame, text="Save",
                   width=18, command=lambda: self.save_vaccine()).grid(row= 14, column=0)
        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def update_vax_info(self,selected):
        print(selected)
        self.inner_frame.destroy()
        self.add_vaccine(selected[1:])
    def update_vaccine(self):
        self.inner_frame = tk.LabelFrame(self.master)
        self.inner_frame.pack(padx=10, pady=10)
        vaccines = my_db.show(f""" SELECT * from Vaccine""")
        print('HERE',vaccines)
        options = tuple()
        print(vaccines)
        if len(vaccines) > 0:

            label = tk.Label(self.inner_frame, text="Vaccines", font=("Arial", 30)).grid(row=0, columnspan=3)
            # create Treeview with 3 columns
            cols = ('Name', 'Available Dose', 'Dose OnHold', 'Company')
            listBox = ttk.Treeview(self.inner_frame, columns=cols, show='headings')

            # set column headings
            for col in cols:
                listBox.heading(col, text=col)
            listBox.grid(row=1, column=0, columnspan=2)
            for i, (name, av_dose, hold_dose,company) in enumerate(vaccines, start=1):
                listBox.insert("", "end", values=(i, name, av_dose, hold_dose,company))
            # tree = event.widget
            # curItem =


            def _element(event):

                tree = event.widget
                for item in tree.selection():
                    print(tree.item(item))
                selection = tree.item(item)["values"]
                showScores = tk.Button(self.inner_frame, text="Update", width=15,
                                       command=lambda: self.update_vax_info(selection)).grid(row=4, column=0)
                return selection


            listBox.bind("<<TreeviewSelect>>", _element)


            for widget in self.inner_frame.children.values():
                widget.grid_configure(padx=50, pady=5)







