import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox
import bcrypt
from nurse import Nurse
import hospitallogic
from hospitallogic import User
from patient import Patient
from admin import Admin
class ScreenLogin:
    def __init__(self, master: themed_tk.ThemedTk):
        self.master = master
        admin = hospitallogic.get_user(email="admin2023@uic.edu", user_type="Admin")
        if len(admin) == 0:
            User(email="admin2023@uic.edu", password="09876", type="Admin").insert()
        self.master.title('Hospital Portal Login')

        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()

        inner_frame = tk.LabelFrame(self.frame)
        inner_frame.pack(padx=10, pady=10)

        self.email = tk.StringVar()
        ttk.Label(inner_frame, text='Email').grid(row=0, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.email).grid(row=1, column=0)

        self.password = tk.StringVar()
        ttk.Label(inner_frame, text='Password').grid(row=2, column=0, sticky='w')
        ttk.Entry(inner_frame, textvariable=self.password).grid(row=3, column=0)

        self.user_type = tk.StringVar()
        ttk.Label(inner_frame, text="User Type").grid(row=4, column=0, sticky='w')
        ttk.Combobox(inner_frame, state="readonly", values=["Patient", "Nurse", "Admin"], textvariable=self.user_type).grid(row=5, column=0)

        ttk.Button(inner_frame, text='Login', width=18, command=self.login).grid(row=6, column=0)
        ttk.Button(inner_frame, text='Sign Up', width=18, command=self.signup).grid(row=7, column=0)

        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)


    def login(self):
        email = self.email.get()
        password = self.password.get()
        user_type = self.user_type.get()
        user = hospitallogic.get_user(email, user_type)
        login_status = False
        if len(user) > 0:
            login_status = bcrypt.checkpw(password.encode('utf-8'), user[0][2].encode('utf-8'))

        if login_status:
            print("Logging in...")
            
            if user_type == "Patient":
                self.frame.destroy()
                patient = Patient(self.master, email)
                patient.show()
            if user_type == "Nurse":
                nurse = Nurse(self.master, email)
                existence = nurse.exist()
                if len(existence) == 0:
                    messagebox.showerror(message="Nurse is not registered")
                else:
                    self.frame.destroy()
                    nurse.show()
            if user_type == "Admin":
                self.frame.destroy()
                Admin(self.master, password)
            else:
                # this case should never be true
                pass
        else:
            messagebox.showerror(message="User not found!")


    def signup(self):
        email = self.email.get()
        password = self.password.get()
        user_type = self.user_type.get()
        user = hospitallogic.get_user(email, user_type)
        check_user_existence = False
        if len(user) > 0:
            check_user_existence = bcrypt.checkpw(password.encode('utf-8'), user[0][2].encode('utf-8'))
        if check_user_existence:
            messagebox.showerror(message="A user with this credential already exists!")
        else:
            print("Signing Up...")
            new_user = hospitallogic.User(email, password, user_type)
            new_user.insert()
            
            if user_type == "Patient":
                self.frame.destroy()
                Patient(self.master, email).show()
            if user_type == "Nurse":
                nurse = Nurse(self.master, email)
                existence = nurse.exist()
                if len(existence) == 0:
                    messagebox.showerror(message="Nurse is not registered")
                else:
                    self.frame.destroy()
                    nurse = nurse.show()
            else:
                # this case should never be true
                pass
