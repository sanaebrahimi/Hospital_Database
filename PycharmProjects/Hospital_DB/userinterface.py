# graphical user interface
import tkinter
from tkinter import ttk

import bcrypt

import hospitallogic as bs
import time
from ttkthemes import themed_tk as tk
from tkinter import messagebox as mb

# inserting into the database
type = ''

def login():
    try:
        user = bs.get_user(e2.get(), type)
        paswd = e3.get()
        login_status = bcrypt.checkpw(paswd.encode('utf-8'), user[0][2].encode('utf-8'))

        if login_status:
            print("Logging in...")
            master.destroy()
            window2_main = tk.ThemedTk()
            window2_main.get_themes()
            window2_main.set_theme('arc')
            window2_main.geometry("800x500")
            window2_main.title("User Portal")
            ttk.Label(window2_main, text="Bye Bye").pack()
            window2_main.mainloop()
        else:
            print("User not found!")
    except IndexError:
        print("Enter you login credential")
def signup():
    try:
        user = bs.get_user(e2.get(), type)
        paswd = e3.get()
        check_user_existence = bcrypt.checkpw(paswd.encode('utf-8'), user[0][2].encode('utf-8'))
        if check_user_existence:
            print('A user with this credential already exists!')
        else:
            signup = bs.User(e2.get(), e3.get(),type)
            signup = signup.insert()
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
master.title("Hospital Portal")
master.geometry("800x500")
# master.

# Labels
ttk.Label(master, text='Email').place(relx = 0.3, rely = 0.5)
ttk.Label(master, text='Password').place(relx = 0.3, rely = 0.6)

# Inputs
# e1 = ttk.Entry(master)
e2 = ttk.Entry(master)
e3 = ttk.Entry(master)

e2.grid(row=10, column=8, padx=2)
e2.place(relx = 0.42, rely = 0.5)

e3.grid(row=11, column=8, padx=2)
e3.place(relx = 0.42, rely = 0.6)

# Buttons

Checkbutton1 = tkinter.IntVar()
Checkbutton2 = tkinter.IntVar()
Checkbutton3 = tkinter.IntVar()

Button1 = ttk.Checkbutton(master, text="Nurse", variable = Checkbutton1, command = set_user_type)
Button1.place(relx = 0.5, rely = 0.65)
Button2 = ttk.Checkbutton(master, text="Patient", variable = Checkbutton2, command = set_user_type)
Button2.place(relx = 0.4, rely = 0.65)
Button3 = ttk.Checkbutton(master, text="Admin", variable = Checkbutton3, command = set_user_type)
Button3.place(relx = 0.6, rely = 0.65)
button = ttk.Button(master, text='Submit', width=18, command=login)
button.place(relx = 0.42, rely = 0.7)
button = ttk.Button(master, text='Sign Up', width=18, command=signup)
button.place(relx = 0.42, rely = 0.75)

tkinter.mainloop()