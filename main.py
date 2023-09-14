import customtkinter as ctk
from connect_serial import *

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("200x500")

text_connect = "Disconnected"


def send():
    print("Sending!")


def connect_plot():
    user_label.configure(text="Connecting", text_color="yellow")
    connect = ConnectSerial("COM3", 9600)
    try:
        connect.connect()
        user_label.configure(text="Connected", text_color="Green")
        print("Connected")
    except:
        user_label.configure(text="Disconnected", text_color="Red")
        print("Not connected")


frame = ctk.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

set_a1 = ctk.CTkEntry(master=frame, placeholder_text="Set a1 angle")
set_a1.pack(pady=12, padx=10)
set_a2 = ctk.CTkEntry(master=frame, placeholder_text="Set a2 angle")
set_a2.pack(pady=12, padx=10)

btn_connect = ctk.CTkButton(master=frame, text="Set angle", command=send)
btn_connect.pack(pady=20)

btn_connect = ctk.CTkButton(master=frame, text="Connect", command=connect_plot)
btn_connect.pack(pady=60)

user_label = ctk.CTkLabel(master=frame, text=text_connect, text_color="Red", pady=50)
user_label.pack()

root.mainloop()
