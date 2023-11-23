from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk as t_tk
from tkinter import messagebox
import bcrypt
import hospital_logic as hl

class ScreenPatientSignup:
    def __init__(self, master: t_tk.ThemedTk, change_screen: Callable[[str], None], hospital_logic: hl.HospitalLogic):
        self.hospital_logic = hospital_logic
        self.master = master
        self.change_screen = change_screen
        self.master.title("Patient Sign Up")

        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()

        self.inner_frame = tk.LabelFrame(self.frame)
        self.inner_frame.pack(padx=10, pady=10)

        self.fname = tk.StringVar()
        ttk.Label(self.inner_frame, text='First Name').grid(row=0, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.fname).grid(row=1, column=0)

        self.lname = tk.StringVar()
        ttk.Label(self.inner_frame, text='Last Name').grid(row=2, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.lname).grid(row=3, column=0)

        self.address = tk.StringVar()
        ttk.Label(self.inner_frame, text='Address').grid(row=0, column=1, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.address).grid(row=1, column=1)

        self.age = tk.StringVar()
        ttk.Label(self.inner_frame, text='Age').grid(row=2, column=1, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.age).grid(row=3, column=1)

        self.gender = tk.StringVar()
        ttk.Label(self.inner_frame, text="Gender").grid(row=8, column=0, sticky='w')
        ttk.Combobox(self.inner_frame, state="readonly", values=["Male", "Female"], textvariable=self.gender).grid(row=9, column=0)

        self.race = tk.StringVar()
        ttk.Label(self.inner_frame, text="Race").grid(row=8, column=1, sticky='w')
        ttk.Combobox(self.inner_frame, state="readonly", values=["Hispanic", "African American", "White"], textvariable=self.race).grid(row=9, column=1)

        self.phone = tk.StringVar()
        ttk.Label(self.inner_frame, text="Phone Number").grid(row=10, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable= self.phone).grid(row=11, column=0)

        self.ssn = tk.StringVar()
        ttk.Label(self.inner_frame, text="SSN").grid(row=10, column=1, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.ssn).grid(row=11, column=1)

        self.occupation = tk.StringVar()
        ttk.Label(self.inner_frame, text='Occupation').grid(row=16, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.occupation).grid(row=17, column=0)

        self.medical_history = tk.StringVar()
        ttk.Label(self.inner_frame, text='Medical History').grid(row=16, column=1, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.medical_history).grid(row=17, column=1)

        self.username = tk.StringVar()
        ttk.Label(self.inner_frame, text="Username").grid(row=18, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.username).grid(row=19, column=0)

        self.password = tk.StringVar()
        ttk.Label(self.inner_frame, text="Password").grid(row=18, column=1, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.password).grid(row=19, column=1)

        ttk.Button(self.inner_frame, text='Sign Up', width=18, command=self.signup).grid(row=20, column=1)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)


    def signup(self):
        user_dict = self.hospital_logic.get_user_info(self.username.get(), "Patient")
        if(0 == len(user_dict)):
            patient_dict = {"SSN": self.ssn.get(),
                            "firstname": self.fname.get(),
                            "lastname": self.lname.get(),
                            "age": self.age.get(),
                            "gender": self.gender.get(),
                            "race": self.race.get(),
                            "occupation": self.occupation.get(),
                            "address": self.address.get(),
                            "phone": self.phone.get(),
                            "medical_history": self.medical_history.get(),
                            "username": self.username.get(),
                            "password": self.password.get()}
            self.hospital_logic.patient_signup(patient_dict)
            self.change_screen("patient_home")
        else:
            messagebox.showerror(message="Username already taken!")