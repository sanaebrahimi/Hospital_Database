from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk as t_tk
from tkinter import messagebox
import hospital_logic as hl

class ScreenAdminSignup:
    def __init__(self, master: t_tk.ThemedTk, routes: Callable[[str], None], hospital_logic: hl.HospitalLogic) -> None:
        self.hospital_logic = hospital_logic
        self.master = master
        self.routes = routes
        self.master.title("Admin Sign Up")

        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()

        self.inner_frame = tk.LabelFrame(self.frame)
        self.inner_frame.pack(padx=10, pady=10)

        self.username = tk.StringVar()
        ttk.Label(self.inner_frame, text="Username").grid(row=0, column=0, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.username).grid(row=1, column=0)

        self.password = tk.StringVar()
        ttk.Label(self.inner_frame, text="Password").grid(row=0, column=1, sticky='w')
        ttk.Entry(self.inner_frame, textvariable=self.password).grid(row=1, column=1)

        ttk.Button(self.inner_frame, text='Sign Up', width=18, command=self.signup).grid(row=2, column=1)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)
    
    def signup(self):
        fields = [self.username.get(), self.password.get()]
        for field in fields:
            if(field == ""):
                messagebox.showerror(message="Please complete all fields!")
                return
        
        self.frame.destroy()
        self.hospital_logic.admin_signup(fields[0], fields[1])
        self.routes("home_admin")