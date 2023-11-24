# graphical user interface
from ttkthemes import themed_tk

import hospital_logic as h_l
import screen_login as s_l
import screen_patientsignup as s_ps
import screen_adminsignup as s_as


class UIController:
    def __init__(self):
        self.master = themed_tk.ThemedTk()
        self.hospital_logic = h_l.HospitalLogic()
        self.current_screen = s_l.ScreenLogin(master=self.master, change_screen=self.login_routes, hospital_logic=self.hospital_logic)
        self.master.mainloop()
    
    # handle login screen routes:
    def login_routes(self, route: str) -> None:
        if(route == "signup_patient"):
            self.current_screen = s_ps.ScreenPatientSignup(master=self.master, change_screen=self.patient_signup_routes, hospital_logic=self.hospital_logic)
        elif(route == "signup_admin"):
            self.current_screen = s_as.ScreenAdminSignup(master=self.master, change_screen=self.admin_signup_routes, hospital_logic=self.hospital_logic)

    # handle patient sign up screen routes
    def patient_signup_routes(self, route: str) -> None:
        if(route == "patient_home"):
            pass
    
    def admin_signup_routes(self, route: str) -> None:
        if(route == "admin_home"):
            pass

UIController()