# graphical user interface
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import messagebox

import screen_login

class UIController:
    def __init__(self):
        self.master = themed_tk.ThemedTk()
        self.current_screen = screen_login.ScreenLogin(master=self.master, change_screen_func=self.login_routes)
        self.master.mainloop()
    
    def login_routes(self, route: str) -> None:
        # handle login page routes to the 3 home page screens:
        pass

UIController()