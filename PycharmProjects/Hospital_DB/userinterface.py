# graphical user interface
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox

import screen_login

class UIController:
    def __init__(self):
        self.master = themed_tk.ThemedTk()
        self.current_screen = screen_login.ScreenLogin(master=self.master)
        self.master.mainloop()
    

UIController()