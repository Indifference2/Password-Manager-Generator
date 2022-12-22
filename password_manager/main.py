import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    data_password = password_entry.get()

    if len(data_password) == 0:
        password_entry.insert(0, password)
        pyperclip.copy(password)
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    data_website = website_entry.get()
    data_email_username = email_username_entry.get()
    data_password = password_entry.get()

    new_data = {
        data_website: {
            "email/username": data_email_username,
            "password": data_password,
        }
    }
    if ((len(data_website) == 0
         or len(data_email_username) == 0
         or len(data_password) == 0)):
        messagebox.showerror("Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=None,
                                       message=f"These are the details entered: \n "
                                               f"Website: {data_website} \n "
                                               f"Email/Username: {data_email_username} \n "
                                               f"Password: {data_password}")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                data_file.close()


def find_password():
    data_website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No Data File Found")
    else:
        if data_website in data:
            password = data[data_website]["password"]
            username_email = data[data_website]["email/username"]
            option = messagebox.askyesno(title=data_website, message=f"Email/Username: {username_email}\n"
                                                                     f"password: {password}\n "
                                                                     "Do you want to copy the password?")
            if option == "Yes":
                pyperclip.copy(password)
                messagebox.showinfo(title=None, message="Copy Successfully")

        else:
            messagebox.showerror(title="Oops", message="No details for the website exists")
    finally:
        data_file.close()


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Password Generator")
root.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = ImageTk.PhotoImage(Image.open("logo.png"))

canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# LABELS

# LABEL WEBSITE
website_label = Label(text="Website")
website_label.grid(row=1, column=0)
# LABEL EMAIL/USERNAME
email_username_label = Label(text="Email/Username:")
email_username_label.grid(row=2, column=0)
# LABEL PASSWORD
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

# ENTRIES

# ENTRY WEBSITE
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2, sticky=W)
website_entry.focus()
# ENTRY EMAIL/USERNAME
email_username_entry = Entry(width=35)
email_username_entry.grid(row=2, column=1, columnspan=2, sticky=W)
# ENTRY PASSWORD
password_entry = Entry(width=25)
password_entry.grid(row=3, column=1, sticky=W)

# BUTTONS

# BUTTON SEARCH
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2)
# BUTTON PASSWORD
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
# BUTTON ADD
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

root.mainloop()
