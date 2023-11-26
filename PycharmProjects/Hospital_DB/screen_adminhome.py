from typing import Callable

import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk as t_tk
from tkinter import messagebox
import hospital_logic as hl

class ScreenAdminHome:
    def __init__(self, master: t_tk.ThemedTk, routes: Callable[[str], None], hospital_logic: hl.HospitalLogic):
        self.hospital_logic = hospital_logic
        self.master = master
        self.routes = routes
        self.master.title('Admin Homepage')

        self.frame = ttk.Frame(self.master, padding=10)
        self.frame.pack()

        inner_frame = tk.LabelFrame(self.frame)
        inner_frame.pack(padx=10, pady=10)
        
        ttk.Button(inner_frame, text='Register Nurse', width=18, command= self.register_nurse).grid(row=4, column=0)  # command=self.login
        ttk.Button(inner_frame, text='Update Nurse Info', width=18, command = self.update_info).grid(row=6, column=0)
        ttk.Button(inner_frame, text='Delete Nurse', width=18, command = self.delete_nurse).grid(row=5, column=0)
        ttk.Button(inner_frame, text='Add Vaccine', width=18).grid(row=4, column=1)  # command=self.signup
        ttk.Button(inner_frame, text='Update Vaccine', width=18).grid(row=7, column=1)  # command=self.signup
        ttk.Button(inner_frame, text='View Nurse', width=18, command = self.view_nurses).grid(row=6, column=1)
        ttk.Button(inner_frame, text='View Patient', width=18).grid(row=5, column=1)  # command=self.signup

        for widget in inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)
    

    def register_nurse(self):
        self.frame.destroy()
        self.routes("signup_nurse")

    def update_info(self):
        pass

    def delete_nurse(self):
        pass

    def view_nurses(self):
        pass