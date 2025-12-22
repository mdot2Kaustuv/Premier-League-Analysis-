import customtkinter as ctk
import tkinter.messagebox as t

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.geometry("800x500")
root.title("Premier League Analysis")


def login() :
    username = "Salah"
    password = "Salahgod"
    #container

    if user_entry.get() == username and u_password.get() == password:
        t.showinfo(title="Login Successful",
                      message="You have logged in Successfully")

    elif user_entry.get() == username and u_password.get() != password:
        t.showwarning(title='Wrong password',
                         message='Please check your password')
    elif user_entry.get() != username and u_password.get() == password:
        t.showwarning(title='Wrong username', message='Please check your username')
    else:
        t.showerror(title="Login Failed", message="Invalid Username and password")




label = ctk.CTkLabel(root,text="Premier League Analysis")
label.pack(pady=20)

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20 , padx = 40 , fill = 'both' , expand = True)

label = ctk.CTkLabel(master=frame,text="Premier League Analysis")
label.pack(pady=12,padx=10)

user_entry= ctk.CTkEntry(master=frame,placeholder_text="Username")
user_entry.pack(pady=12,padx=10)

u_password= ctk.CTkEntry(master=frame,placeholder_text="Password",show="*")
u_password.pack(pady=12,padx=10)


button = ctk.CTkButton(master=frame,text='Login',command=login)
button.pack(pady=12,padx=10)

checkbox = ctk.CTkCheckBox(master=frame,text='Remember Me')
checkbox.pack(pady=12,padx=10)

root.mainloop()




