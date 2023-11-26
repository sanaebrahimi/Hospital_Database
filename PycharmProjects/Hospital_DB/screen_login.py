import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk as t_tk
from tkinter import messagebox

from typing import Callable

import hospital_logic as hl

class ScreenLogin:
    def __init__(self, master: t_tk.ThemedTk, routes: Callable[[str], None], hospital_logic: hl.HospitalLogic):
        self.hospital_logic = hospital_logic
        self.master = master
        self.routes = routes
        self.master.title('Hospital Portal Login')

        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()

        inner_frame = tk.LabelFrame(self.frame)
        inner_frame.pack(padx=10, pady=10)

        self.username_var = tk.StringVar()
        ttk.Label(inner_frame, text='Username').grid(row=0, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.username_var).grid(row=1, column=0)

        self.password_var = tk.StringVar()
        ttk.Label(inner_frame, text='Password').grid(row=2, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.password_var).grid(row=3, column=0)

        self.user_type_var = tk.StringVar()
        ttk.Label(inner_frame, text="User Type").grid(row=4, column=0, sticky='w')
        ttk.Combobox(inner_frame, state="readonly", values=["Patient", "Nurse", "Admin"], textvariable=self.user_type_var).grid(row=5, column=0)

        ttk.Button(inner_frame, text='Login', width=18, command=self.login).grid(row=6, column=0)
        ttk.Label(inner_frame, text="Or...").grid(row=7, column=0)
        ttk.Button(inner_frame, text='Patient Sign Up', width=18, command=self.signup_patient).grid(row=8, column=0)
        ttk.Button(inner_frame, text='Admin Sign Up', width=18, command=self.signup_admin).grid(row=9, column=0)

        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)


    def login(self) -> None:
        user_type = self.user_type_var.get()
        user_dict = self.hospital_logic.get_user_info(self.username_var.get(), user_type)
        if(0 != len(user_dict)):
            if(self.hospital_logic.is_password_valid(password=self.password_var.get(), hash=user_dict["Password"])):
                print("Logging in...")
                self.frame.destroy()
                if user_type == "Patient":
                    self.routes("home_patient")
                elif user_type == "Nurse":
                    self.routes("home_nurse")
                elif user_type == "Admin":
                    self.routes("home_admin")
                else:
                    # this case should never be true
                    print("Unknown user_type")
            else:
                messagebox.showerror(message="Password Incorrect!")
        else:
            messagebox.showerror(message="Username not found!")

    def signup_patient(self) -> None:
        self.frame.destroy()
        self.routes("signup_patient")

    def signup_admin(self) -> None:
        admin_dict = self.hospital_logic.get_admin_info()
        if(0 == len(admin_dict)):
            self.frame.destroy()
            self.routes("signup_admin")
        else:
            messagebox.showerror(message="There can only be one Admin!")
