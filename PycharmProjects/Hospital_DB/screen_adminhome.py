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

        self.inner_frame = tk.LabelFrame(self.frame)
        self.inner_frame.pack(padx=10, pady=10)
        
        self.nurse_canvas = tk.Canvas(self.inner_frame)
        self.nurse_canvas.grid(row=0, column=0)

        self.nurse_tree = ttk.Treeview(self.nurse_canvas)
        self.populate_nurse_canvas()
        

        self.vaccine_canvas = tk.Canvas(self.inner_frame)
        self.vaccine_canvas.grid(row=0, column=1)

        self.vaccine_tree = ttk.Treeview(self.vaccine_canvas)
        self.populate_vaccine_canvas()
        # 
        # 
        
        # ttk.Button(inner_frame, text='View Patient', width=18).grid(row=5, column=1)



    def populate_vaccine_canvas(self):
        vaccine_list = self.hospital_logic.get_vaccines()
        if(0 != len(vaccine_list)):
            columns = list(vaccine_list[0].keys())
            self.vaccine_tree["columns"] = columns

            self.vaccine_tree.column('#0', width=0, stretch=tk.NO)
            for field in columns:
                self.vaccine_tree.column(field, width=60, anchor=tk.W)
            
            for field in columns:
                self.vaccine_tree.heading(field, text=field, anchor='w')
            
            for vaccine in vaccine_list:
                values = [vaccine[field] for field in columns]
                self.vaccine_tree.insert('', 'end', values=values)
        
        self.vaccine_tree.grid(row=0, column=0, rowspan=10, columnspan=2)
        ttk.Button(self.vaccine_canvas, text='Add Vaccine', width=18, command=self.add_vaccine).grid(row=11, column=0)
        ttk.Button(self.vaccine_canvas, text='Update Vaccine', width=18, command=self.update_vaccine).grid(row=11, column=1)

        for widget in self.vaccine_canvas.children.values():
            widget.grid_configure(padx=5, pady=5)

    def add_vaccine(self):
        self.frame.destroy()
        self.routes("add_vaccine")
    
    def update_vaccine(self):
        pass


    def populate_nurse_canvas(self):
        nurse_list = self.hospital_logic.get_nurses()
        if(0 != len(nurse_list)):
            columns = list(nurse_list[0].keys())
            self.nurse_tree["columns"] = columns

            self.nurse_tree.column('#0', width=0, stretch=tk.NO)
            for field in columns:
                self.nurse_tree.column(field, width=60, anchor=tk.W)
            
            for field in columns:
                self.nurse_tree.heading(field, text=field, anchor='w')
            
            for nurse in nurse_list:
                values = [nurse[field] for field in columns]
                self.nurse_tree.insert('', 'end', values=values)
        
        self.nurse_tree.grid(row=0, column=0, rowspan=10, columnspan=4)
        ttk.Button(self.nurse_canvas, text='Register new Nurse', width=20, command=self.register_nurse).grid(row=11, column=0)
        ttk.Button(self.nurse_canvas, text='Update Nurse Info', width=18, command = self.update_info).grid(row=11, column=1)
        ttk.Button(self.nurse_canvas, text='Delete Nurse', width=18, command = self.delete_nurse).grid(row=11, column=2)
        ttk.Button(self.nurse_canvas, text='View Nurse Scheduling', width=23, command = self.view_nurses).grid(row=11, column=3)

        for widget in self.nurse_canvas.children.values():
            widget.grid_configure(padx=5, pady=5)



    def register_nurse(self):
        self.frame.destroy()
        self.routes("signup_nurse")

    def update_info(self):
        pass

    def delete_nurse(self):
        pass

    def view_nurses(self):
        pass