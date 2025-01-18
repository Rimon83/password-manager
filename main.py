import os
import sys
import tkinter
import random
import pyperclip
from tkinter import messagebox
from tkinter_components import EntryComponent, LabelComponent, ButtonComponent, CanvasComponent, TextComponent
from file_handle import FileHandle

# PINK = "#e2979c"
# RED = "#e7305b"
# GREEN = "#9bdeac"
text_colors = ["#e2979c", "#9bdeac", "#E7D283"]
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
FILE_NAME = "password.txt"
ROWS = 4
COLUMNS = 3
text_row = 0


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS2
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# generate password
def generate_password():
    password = ""
    password_list = []
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y' 'z']
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']',
               '|', '\\', ';', ':', "'", '"', '<', '>', ',', '.', '/', '?', '`', '~']
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # generate 4 letters
    password_letters = [random.choice(letters) for _ in range(4)]
    password_numbers = [str(random.choice(numbers)) for _ in range(4)]
    password_symbols = [random.choice(symbols) for _ in range(4)]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    # change the list into string
    password = ''.join(password_list)
    password_entry.delete(0, tkinter.END)
    password_entry.config(fg="black")
    password_entry.insert(0, string=password)
    # to automatically copy the password once is written or generated in password entry
    pyperclip.copy(password)


def handle_add_button():
    if website_entry.get_value() == "" or password_entry.get_value() == "" or email_entry.get_value() == "":
        messagebox.showwarning(title="Oops", message="Please all fields are required")
        return

    if add_button["text"] == "Add":
        is_ok = messagebox.askokcancel(title="Website", message=f"These your information:\n "
                                                                f"website: {website_entry.get()}\n"
                                                                f"email: {email_entry.get()}\n"
                                                                f"password: {password_entry.get()}\n"
                                                                f"Are sure to save?")
        if is_ok:
            file = FileHandle(resource_path(FILE_NAME))
            file.append_to_file([f"{website_entry.get().title()} | {email_entry.get()} | "
                                 f"{password_entry.get()}"])

    if add_button["text"] == "Update":
        is_ok = messagebox.askokcancel(title="Website", message=f"These your information:\n "
                                                                f"website: {website_entry.get()}\n"
                                                                f"email: {email_entry.get()}\n"
                                                                f"password: {password_entry.get()}\n"
                                                                f"Are sure to update?")
        if is_ok:
            file = FileHandle(resource_path(FILE_NAME))
            key_search = website_entry.get().title()
            new_data = f"{website_entry.get().title()} | {email_entry.get()} | {password_entry.get()}"
            file.update_file(key_search, new_data)
    # update the text area
    create_text(frame_display)

    # delete all input value
    website_entry.reset_entry("www.example.com")
    email_entry.reset_entry("john@gmail.com")
    password_entry.reset_entry("Enter Password")
    add_button.edit_text_button("Add")
    website_entry.focus()


def handle_search():
    website_input = website_entry.get().title()
    with open(resource_path("password.txt")) as file:
        for line in file:
            credentials_auth = [auth for auth in line.strip().split(" | ")]

        website_name = credentials_auth[0]

        if website_name != website_input:
            messagebox.showwarning(title="Oops", message="The website does not match with "
                                                         "stored data")
            return

        if website_name == website_input:
            website_entry.set_entry(credentials_auth[0])
            email_entry.set_entry((credentials_auth[1]))
            password_entry.set_entry(credentials_auth[2])
            add_button.edit_text_button("Update")


# handle delete one line from file
def handle_delete_line(index):
    open_file = FileHandle(FILE_NAME)
    with open(FILE_NAME) as file:
        lines = [line.strip() for line in file]
        words = [word for word in lines[index].split(" | ")]
        is_ok = messagebox.askokcancel(title="Website", message=f"These your information:\n "
                                                                f"website: {words[0]}\n"
                                                                f"email: {words[1]}\n"
                                                                f"password: {words[2]}\n"
                                                                f"Are sure to Delete?")
        if is_ok:
            open_file.delete_line(index)
            create_text(frame_display)


# Delete all widgets in specific frame
def clear_frame_widgets(frame_name):
    for widget in frame_name.winfo_children():  # Remove old widgets
        widget.destroy()


def create_text(display_frame):
    clear_frame_widgets(display_frame)
    #  Create a Scrollable Canvas inside `display_frame`
    scrollbar_canvas = CanvasComponent(display_frame, width=800, row=0, column=0, sticky="nsew")

    #  Create a frame inside the canvas for Text widgets
    text_frame = tkinter.Frame(scrollbar_canvas)
    scrollbar_canvas.create_scrollbar_grid(text_frame)
    try:
        with open(FILE_NAME) as file:
            contents = [line.strip() for line in file]
            total_label.set_label(f"Total: {len(contents)}")

        for (row, line) in enumerate(contents):
            single_data = [data for data in line.split(" | ")]
            for (column, word) in enumerate(single_data):
                text = TextComponent(text_frame, width=20, height=1, bg=text_colors[column], font=("Arial", 12),
                                     row=row + 1,
                                     column=column, padx=10, pady=10)
                text.config(padx=10)
                text.insert("end", word)
                text.config(state="disabled")  # Prevents user editing
            """
            lambda r=row: handle_delete_line(r) creates a function that captures the current value of row and 
            executes handle_delete_line(row) only when the button is clicked.
            r=row ensures that each button remembers the correct row index.
            """
            delete_button = ButtonComponent(text_frame, text="Delete", width=10, bg="#e7305b", fg="#fff", row=row + 1,
                                            column=3, command=lambda r=row: handle_delete_line(r))
    except FileNotFoundError:
        total_label.set_label(f"There is no data to list")




window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=YELLOW)

# create frame
main_frame = tkinter.Frame(window)
main_frame.config(bg=YELLOW)
# canvas
canvas = CanvasComponent(main_frame, width=200, height=200, row=0, column=1)
canvas.create_canvas_image(x_coor=100, y_coor=100, image=resource_path("logo.png"))
canvas.config(bg=YELLOW)
# website

website_label = LabelComponent(main_frame, text="Website:", font=("Arial", 12, "bold"), row=1, column=0, bg=YELLOW)
website_label.config(pady=10)
website_entry = EntryComponent(main_frame, width=23, font=("Arial", 14), row=1,
                               column=1, placeholder="www.example.com")
website_entry.focus()
search_button = ButtonComponent(main_frame, text="Search", width=15, bg="blue", fg="white",
                                font=("Arial", 10), row=1, column=2, command=handle_search)
#
# #email
email_label = LabelComponent(main_frame, text="Email/Username:", font=("Arial", 12, "bold"),
                             row=2, column=0, bg=YELLOW)
email_label.config(pady=10)
email_entry = EntryComponent(main_frame, width=35, font=("Arial", 14), row=2,
                             column=1, columnspan=2, placeholder="john@gmail.com")

# password
password_label = LabelComponent(main_frame, text="Password:", font=("arial", 12, "bold"),
                                row=3, column=0, bg=YELLOW)
password_label.config(pady=10)
password_entry = EntryComponent(main_frame, width=23, font=("Arial", 14), row=3,
                                column=1, placeholder="Enter Password")
password_button = ButtonComponent(main_frame, text="Generate Password", width=15, row=3,
                                  column=2, font=("Arial", 10), command=generate_password)

# add button
add_button = ButtonComponent(main_frame, text="Add", width=48, row=4, column=1, columnspan=2, command=handle_add_button)
main_frame.pack(pady=30)

# this way if we don't use frame
# for row in range(ROWS):
#     window.grid_rowconfigure(row, weight=1)
#
#
# for column in range(COLUMNS):
#     window.grid_columnconfigure(column, weight=1)

# frame for credential title
frame_title = tkinter.Frame(window, bg=YELLOW)
data_label = LabelComponent(frame_title, text="Your credential list:", font=("Arial", 12, "bold"),
                            row=0, column=0, bg=YELLOW)
total_label = LabelComponent(frame_title, text="Total:", font=("Arial", 10, "bold"), row=1, column=0, bg=YELLOW, fg="gray")
frame_title.pack(pady=20)

frame_display = tkinter.Frame(window)
frame_display.config(bg=YELLOW)
create_text(frame_display)
frame_display.pack()

window.mainloop()


