# graphical user interface
from ttkthemes import themed_tk

import hospital_logic as h_l
import screen_login as s_l
import screen_patientsignup as s_ps
import screen_adminsignup as s_as
import screen_nursesignup as s_ns
import screen_adminhome as s_ah
import screen_addvaccine as s_av

class UIController:
    def __init__(self):
        self.master = themed_tk.ThemedTk()
        self.hospital_logic = h_l.HospitalLogic()
        self.current_screen = s_l.ScreenLogin(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        self.master.mainloop()
    
    # handle screen routes:
    def routes(self, route: str) -> None:
        if(route == "signup_patient"):
            self.current_screen = s_ps.ScreenPatientSignup(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        elif(route == "signup_admin"):
            self.current_screen = s_as.ScreenAdminSignup(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        elif(route == "signup_nurse"):
            self.current_screen = s_ns.ScreenNurseSignup(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        elif(route == "home_admin"):
            self.current_screen = s_ah.ScreenAdminHome(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)
        elif(route == "home_patient"):
            pass
        elif(route == "add_vaccine"):
            self.current_screen = s_av.ScreenAddVaccine(master=self.master, routes=self.routes, hospital_logic=self.hospital_logic)

UIController()