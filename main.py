import customtkinter
# import customtkinter as ctk
from connect_serial import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode("Dark")
        self.title("Plot_C Control GUI")
        self.geometry(f"{300}x{500}")
        self.text_connect = "Disconnected"
        self.set_a1 = customtkinter.CTkEntry(master=self, placeholder_text="Set a1 angle")
        self.set_a1.pack(pady=20, padx=4)
        self.set_a2 = customtkinter.CTkEntry(master=self, placeholder_text="Set a2 angle")
        self.set_a2.pack(pady=8, padx=4)
        self.btn_connect = customtkinter.CTkButton(master=self, text="Set angle", command=self.send)
        self.btn_connect.pack(pady=20)
        self.user_label = customtkinter.CTkLabel(master=self, text=self.text_connect, text_color="Red", pady=50)
        self.user_label.pack()
        self.btn_connect = customtkinter.CTkButton(master=self, text="Connect", command=self.connect_plot)
        self.btn_connect.pack(pady=50, padx=10)

    def connect_plot(self):
        connect = ConnectSerial("COM3", 9600)
        print('connecting...')
        try:
            connect.connect()
        except ConnectionError:
            pass

    def send(self):
        print("Sending!")


# ctk.set_default_color_theme("dark-blue")
#
if __name__ == "__main__":
    app = App()
    app.mainloop()
