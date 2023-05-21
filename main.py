import sqlite3
from tkinter import *
import random

#----------------------------------------------------------------settings----------------------------------------------------------------#
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','!', '#', '$', '%', '&', '(', ')', '*', '+']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def toggle_visibility():
    if Password_entry.cget('show') == '':
        Password_entry.configure(show='*')
        view_pass.configure(image=view_image)
    else:
        Password_entry.configure(show='')
        view_pass.configure(image=hide_image)
    
    
def suggest_password():
    password = ''
    for _ in range(12):
        tmp_pass = random.choice([letters,numbers,symbols])
        password += random.choice(tmp_pass)
    Password_entry.delete(0, END)
    Password_entry.insert(END, password)

conn = sqlite3.connect('mydatabase.db')
def show_password():
    username_value = Web_entry.get()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username_value,))
    password = cursor.fetchone()
    Password_entry.delete(0, END)
    if password is not None:
        Password_entry.insert(0, password[0])
    else:
        Password_entry.insert(0, 'Username not found')
# create a table to store login credentials
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

# define a function to insert login credentials into the database
def insert_login():
    username_value = Web_entry.get()
    password_value = Password_entry.get()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username_value, password_value))
    conn.commit()
    
def update_password():
    username_value = Web_entry.get()
    password_value = Password_entry.get()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password = ? WHERE username = ?', (password_value, username_value))
    conn.commit()


#----------------------------------------------------Ui--------------------------------------#
root = Tk()
root.title("Password Manager")
root.geometry('500x400+700+300')


#main window icon
main_icon = PhotoImage(file='images/main_ico.png')
root.iconphoto(False, main_icon)
root.configure(bg='white')
root.resizable(False,False)

#header
header_image = PhotoImage(file='images/password_manager.png')
header_label = Label(image=header_image,bg="#FFFFFF").place(x=90,y=0,)

# create input fields for the dictionary keys and values
Web_label = Label(root, text="Enter website url",bg="#FFFFFF")
Web_label.place(x=20, y=90)
Web_entry = Entry(root)
Web_entry.place(x=300, y=90)

Password_label = Label(root, text="Enter your password",bg="#FFFFFF")
Password_label.place(x=20, y=150)
Password_entry = Entry(root)
Password_entry.config(show="*")
Password_entry.place(x=300, y=150)

#show password
view_image = PhotoImage(file='images/view_icon.png')
hide_image = PhotoImage(file='images/hide_icon.png')
view_pass = Button(root, image=view_image, command=toggle_visibility)
view_pass.place(x=450,y=150)
# create a "save" button

save_button = Button(root, text='Save password', bg="#FFFFFF",command=insert_login)
save_button.place(x=30, y=250)

# start the tkinter event loop

show_password_button = Button(root, text='Show Password',bg="#FFFFFF", command=show_password)
show_password_button.place(x=130,y=250)

update_password_button = Button(root, text='Update Password',bg="#FFFFFF", command=update_password).place(x=230,y=250)

suggest_password = Button(root, text='Suggest password',bg="#FFFFFF", command=suggest_password).place(x=340,y=250)

root.mainloop()
conn.close()