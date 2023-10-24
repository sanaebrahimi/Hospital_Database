# graphical user interface
import tkinter
from tkinter import ttk
import hospitallogic as bs
import time
from ttkthemes import themed_tk as tk
from tkinter import messagebox as mb

# inserting into the database
type = ''

def login():
    try:
        login = bs.User(e2.get(), e3.get(),type)
        login_status = login.get_user()
        print(login_status)
    except IndexError:
        mb.showerror(" Enter you login credential")
def signup():
    try:
        signup = bs.User(e2.get(), e3.get(),type)
        login_status = signup.insert()
        print(login_status)
    except IndexError:
        mb.showerror(" Enter you login credential")

def set_user_type():
    global type
    if Checkbutton1.get():
        type = 'nurse'
    elif Checkbutton2.get():
        type = 'patient'
    elif Checkbutton3.get():
        type = 'admin'

def f():
    try:
        pr = bs.User(e1.get(), e2.get(), e3.get(), e4.get())
        output_error = pr.insert()
    except IndexError:
        mb.showerror("BAM", "You didn't buy anything!")

# showing what each customer bought
def g():
    list_of_items = bs.Product.show()
    Lb = tkinter.Listbox(master, width = 30)
    for i, item in enumerate(list_of_items):
        Lb.insert(i, (item[0], item[1], item[2], item[3]))
        Lb.grid(row=3, column=3)

# showing the history of products that a customer bought
def purchase_history():
    try:
        full_name = e4.get()
        purchase_hist = bs.Product.show_history(full_name.split(" "))
        Lb = tkinter.Listbox(master, width = 20)
        for i, item in enumerate(purchase_hist):
            Lb.insert(i, (item[0], item[1]))
            Lb.grid(row=3, column=18)
    except IndexError:
        mb.showerror("BAM", "Sorry, nothing to show!")

# setting the Adapta theme
master = tk.ThemedTk()
master.get_themes()
master.set_theme('arc')
# master.

# Labels
ttk.Label(master, text='Username').grid(row=0, column=2)
ttk.Label(master, text='Email').grid(row=1, column=2)
ttk.Label(master, text='Password').grid(row=2, column=2)
# ttk.Label(master, text='User Type').grid(row=0, column=17)

# Inputs
e1 = ttk.Entry(master)
e2 = ttk.Entry(master)
e3 = ttk.Entry(master)
# e4 = ttk.Entry(master)

e1.grid(row=0, column=3, padx=2)
e2.grid(row=1, column=3, padx=2)
e3.grid(row=2, column=3, padx=2)
# e4.grid(row=0, column=18, padx=2)

# Buttons

Checkbutton1 = tkinter.IntVar()
Checkbutton2 = tkinter.IntVar()
Checkbutton3 = tkinter.IntVar()

Button1 = ttk.Checkbutton(master, text="Nurse", variable = Checkbutton1, command = set_user_type)
Button1.grid(row=0, column=17)
Button2 = ttk.Checkbutton(master, text="Patient", variable = Checkbutton2, command = set_user_type)
Button2.grid(row=0, column=18)
Button3 = ttk.Checkbutton(master, text="Admin", variable = Checkbutton3, command = set_user_type)
Button3.grid(row=0, column=19)
button = ttk.Button(master, text='Submit', width=18, command=login)
button.grid(row=2, column=18)
button = ttk.Button(master, text='Sign Up', width=18, command=signup())
button.grid(row=1, column=18)

tkinter.mainloop()