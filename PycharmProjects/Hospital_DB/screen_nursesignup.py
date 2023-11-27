from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk as t_tk
from tkinter import messagebox
import hospital_logic as hl

class ScreenNurseSignup:
    def __init__(self, master: t_tk.ThemedTk, routes: Callable[[str], None], hospital_logic: hl.HospitalLogic):
        self.hospital_logic = hospital_logic
        self.master = master
        self.routes = routes
        self.master.title('Nurse Sign Up')

        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()

        inner_frame = tk.LabelFrame(self.frame)
        inner_frame.pack(padx=10, pady=10)
        
        self.fname = tk.StringVar()
        ttk.Label(inner_frame, text='First Name').grid(row=0, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.fname).grid(row=1, column=0)

        self.lname = tk.StringVar()
        ttk.Label(inner_frame, text='Last Name').grid(row=2, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.lname).grid(row=3, column=0)
        
        self.address = tk.StringVar()
        ttk.Label(inner_frame, text='Address').grid(row=4, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.address).grid(row=5, column=0)
        
        self.age = tk.StringVar()
        ttk.Label(inner_frame, text='Age').grid(row=6, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.age).grid(row=7, column=0)

        self.gender = tk.StringVar()
        ttk.Label(inner_frame, text="Gender").grid(row=8, column=0, sticky='w')
        ttk.Combobox(inner_frame, state="readonly", values=["Male", "Female"], textvariable=self.gender).grid(row=9, column=0)

        self.phone = tk.StringVar()
        ttk.Label(inner_frame, text="Phone Number").grid(row=10, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.phone).grid(row=11, column=0)

        self.username = tk.StringVar()
        ttk.Label(inner_frame, text="Username").grid(row=12, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.username).grid(row=13, column=0)

        self.password = tk.StringVar()
        ttk.Label(inner_frame, text="Password").grid(row=14, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.password).grid(row=15, column=0)

        ttk.Button(inner_frame, text='Submit', width=18, command = self.submit).grid(row=16, column=0)

        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)

    def submit(self):
        fields = [self.username.get(), self.password.get(), self.fname.get(), self.lname.get(),
                  self.address.get(), self.phone.get(), self.age.get(), self.gender.get()]
        for field in fields:
            if(field == ""):
                messagebox.showerror(message="Please complete all fields!")
                return
        
        user_dict = self.hospital_logic.get_user_info(username=fields[0], user_type="Nurse")

        if(0 == len(user_dict)):
            self.frame.destroy()
            self.hospital_logic.nurse_signup(fields[0], fields[1], fields[2], fields[3],
                                             fields[4], fields[5], fields[6], fields[7])
            self.routes("home_admin")
        else:
            messagebox.showerror(message="Username already taken!")