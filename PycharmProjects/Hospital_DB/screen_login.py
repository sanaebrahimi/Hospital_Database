from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox
import bcrypt

import hospitallogic


class ScreenLogin:
    def __init__(self, master: themed_tk.ThemedTk, change_screen_func: Callable[[str], None]):
        self.master = master
        self.change_screen = change_screen_func
        self.master.title('Hospital Portal Login')

        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()

        inner_frame = tk.LabelFrame(self.frame)
        inner_frame.pack(padx=10, pady=10)

        self.email_var = tk.StringVar()
        ttk.Label(inner_frame, text='Email').grid(row=0, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.email_var).grid(row=1, column=0)

        self.password_var = tk.StringVar()
        ttk.Label(inner_frame, text='Password').grid(row=2, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.password_var).grid(row=3, column=0)

        self.user_type_var = tk.StringVar()
        ttk.Label(inner_frame, text="User Type").grid(row=4, column=0, sticky='w')
        ttk.Combobox(inner_frame, state="readonly", values=["Patient", "Nurse", "Admin"], textvariable=self.user_type_var).grid(row=5, column=0)

        ttk.Button(inner_frame, text='Login', width=18, command=self.login).grid(row=6, column=0)
        ttk.Button(inner_frame, text='Sign Up', width=18, command=self.signup).grid(row=7, column=0)

        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)


    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()
        user_type = self.user_type_var.get()
        try:
            user = hospitallogic.get_user(email, user_type)
            login_status = bcrypt.checkpw(password.encode('utf-8'), user[0][2].encode('utf-8'))

            if login_status:
                print("Logging in...")
                self.frame.destroy()
                match user_type:
                    case "Patient":
                        self.change_screen("home_patient")
                    case "Nurse":
                        self.change_screen("home_nurse")
                    case "Admin":
                        self.change_screen("home_admin")
                    case _:
                        # this case should never be true
                        pass
            else:
                print("User not found!")
        except IndexError:
            messagebox.showerror(message="Enter your login credentials")


    def signup(self):
        email = self.email_var.get()
        password = self.password_var.get()
        user_type = self.user_type_var.get()
        try:
            user = hospitallogic.get_user(email, user_type)
            check_user_existence = bcrypt.checkpw(password.encode('utf-8'), user[0][2].encode('utf-8'))
            if check_user_existence:
                print('A user with this credential already exists!')
            else:
                print("Signing Up...")
                new_user = hospitallogic.User(email, password, user_type)
                new_user.insert()
                self.frame.destroy()
                match user_type:
                    case "Patient":
                        self.change_screen("home_patient")
                    case "Nurse":
                        self.change_screen("home_nurse")
                    case "Admin":
                        self.change_screen("home_admin")
                    case _:
                        # this case should never be true
                        pass
        except IndexError:
            messagebox.showerror(message="Enter your login credentials")