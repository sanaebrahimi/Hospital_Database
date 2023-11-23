# graphical user interface
from ttkthemes import themed_tk

import hospital_logic as h_l
import screen_login as s_l
import screen_patientsignup as s_ps


class UIController:
    def __init__(self):
        self.master = themed_tk.ThemedTk()
        self.hospital_logic = h_l.HospitalLogic()
        self.current_screen = s_l.ScreenLogin(master=self.master, change_screen=self.login_routes, hospital_logic=self.hospital_logic)
        self.master.mainloop()
    
    def login_routes(self, route: str) -> None:
        # handle login screen routes:
        if(route == "signup_patient"):
            self.current_screen = s_ps.ScreenPatientSignup(master=self.master, change_screen=self.patient_signup, hospital_logic=self.hospital_logic)

    def patient_signup(self, route: str) -> None:
        # handle patient sign up screen routes
        if(route == "patient_home"):
            pass

UIController()