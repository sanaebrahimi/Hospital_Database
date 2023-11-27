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
        
        self.create_nurse_canvas()
        
        # ttk.Button(inner_frame, text='Add Vaccine', width=18).grid(row=4, column=1)
        # ttk.Button(inner_frame, text='Update Vaccine', width=18).grid(row=7, column=1)
        
        # ttk.Button(inner_frame, text='View Patient', width=18).grid(row=5, column=1)

        for widget in self.inner_frame.children.values():
            widget.grid_configure(padx=50, pady=5)
    

    def create_nurse_canvas(self):
        canvas = tk.Canvas(self.inner_frame)
        canvas.pack(padx=10, pady=10)

        tree = ttk.Treeview(canvas)

        nurse_list = self.hospital_logic.get_nurses()

        if(0 != len(nurse_list)):
            columns = list(nurse_list[0].keys())
            tree["columns"] = columns

            tree.column('#0', width=0, stretch=tk.NO)
            for field in columns:
                tree.column(field, width=60, anchor=tk.W)

            
            for field in columns:
                tree.heading(field, text=field, anchor='w')
            
            for nurse in nurse_list:
                values = [nurse[field] for field in columns]
                tree.insert('', 'end', values=values)
        
        tree.grid(row=0, column=0, rowspan=10, columnspan=4)
        ttk.Button(canvas, text='Register new Nurse', width=18, command=self.register_nurse).grid(row=11, column=0)
        ttk.Button(canvas, text='Update Nurse Info', width=18, command = self.update_info).grid(row=11, column=1)
        ttk.Button(canvas, text='Delete Nurse', width=18, command = self.delete_nurse).grid(row=11, column=2)
        ttk.Button(canvas, text='View Nurse Scheduling', width=23, command = self.view_nurses).grid(row=11, column=3)

        for widget in canvas.children.values():
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