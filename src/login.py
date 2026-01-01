import customtkinter as ctk
import tkinter.messagebox as t
from PIL import Image
import re


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry("800x500")
root.title("Premier League Analysis")


def login() :
    email = user_entry.get()
    passwd = u_password.get()
    #container

    if user_entry.get() == email and u_password.get() == passwd:
        t.showinfo(title="Login Successful",
                      message="You have logged in Successfully")

    elif user_entry.get() == email and u_password.get() != passwd :
        t.showwarning(title='Wrong password',
                         message='Please check your password')
    elif user_entry.get() != email and u_password.get() == passwd :
        t.showwarning(title='Wrong username', message='Please check your username')
    else:
        t.showerror(title="Login Failed", message="Invalid Username and password")

def signup() :
    username = user_entry.get()
    if username == "":
        t.showwarning(title="Empty Fields", message="Please enter a Email to sign up")
    else:
        t.showinfo(title="Sign Up", message=f"Registration page for {username} coming soon!")


my_image = ctk.CTkImage(light_image=Image.open("logo.jpg"),
                         dark_image=Image.open("logo.jpg"),
                         size=(200, 150))


image_label = ctk.CTkLabel(master=root , image=my_image, text="")
image_label.pack(pady=12, padx=10)


frame = ctk.CTkFrame(master=root)
frame.pack(pady=20 , padx = 40 , fill = 'both' , expand = True)

custom_font = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")

label = ctk.CTkLabel(master=frame,text="Premier League Analysis",font=custom_font)
label.pack(pady=12,padx=10)

user_entry= ctk.CTkEntry(master=frame,placeholder_text="Enter Your Email Address")
user_entry.pack(pady=12,padx=10)

u_password= ctk.CTkEntry(master=frame,placeholder_text="Custom Password",show="*")
u_password.pack(pady=12,padx=10)

button_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
button_frame.pack(pady=20)

login_button = ctk.CTkButton(master=button_frame, text='Login', width=140, command=login)
login_button.grid(row=0, column=0, padx=10)

signup_button = ctk.CTkButton(master=button_frame, text='Sign Up', width=140,
                             fg_color="transparent", border_width=2,
                             text_color=("black", "white"), command=signup)
signup_button.grid(row=0, column=1, padx=10)

checkbox = ctk.CTkCheckBox(master=frame,text='Remember Me')
checkbox.pack(pady=12,padx=10)

root.mainloop()




