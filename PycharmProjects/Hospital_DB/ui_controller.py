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
        self.current_screen = s_l.ScreenLogin(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        self.master.mainloop()
    
    # handle login screen routes:
    def routes(self, route: str) -> None:
        if(route == "signup_patient"):
            self.current_screen = s_ps.ScreenPatientSignup(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        elif(route == "signup_admin"):
            self.current_screen = s_as.ScreenAdminSignup(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        elif(route == "home_admin"):
            pass
        elif(route == "home_patient"):
            pass

UIController()