import customtkinter
from connect_serial import *
import serial.tools.list_ports


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self._set_appearance_mode("Dark")
        self.connection = None
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.title("Plot_C Control GUI")
        self.geometry(f"{300}x{744}")
        self.text_connect = "Disconnected"
        self.set_a1 = customtkinter.CTkEntry(master=self, placeholder_text="Set a1 angle")
        self.set_a1.pack(pady=20, padx=4)
        self.set_a2 = customtkinter.CTkEntry(master=self, placeholder_text="Set a2 angle")
        self.set_a2.pack(pady=8, padx=4)
        self.btn_connect = customtkinter.CTkButton(master=self, text="Set angle", command=self.send)
        self.btn_connect.pack(pady=20)
        self.user_label = customtkinter.CTkLabel(master=self, text=self.text_connect, text_color="Red", pady=50)
        self.user_label.pack()

        self.btn_connect = customtkinter.CTkButton(master=self, text="Tap", command=self.tap)
        self.btn_connect.pack(pady=5, padx=10)
        self.btn_connect = customtkinter.CTkButton(master=self, text="Start", command=self.start)
        self.btn_connect.pack(pady=5, padx=10)
        self.btn_connect = customtkinter.CTkButton(master=self, text="Cancel", command=self.cancel)
        self.btn_connect.pack(pady=5, padx=10)
        self.btn_connect = customtkinter.CTkButton(master=self, text="Home", command=self.home)
        self.btn_connect.pack(pady=5, padx=10)

        self.btn_connect = customtkinter.CTkButton(master=self, text="Connect", command=self.connect_plot)
        self.btn_connect.pack(ipady=30, padx=10, pady=30)
        self.get_port = serial.tools.list_ports.comports()
        list_port = []
        for port, desc, hwid in sorted(self.get_port):
            list_port.append(port)
        self.combo_box = customtkinter.CTkComboBox(master=self,
                                                   values=list_port)
        self.combo_box.pack(pady=5, padx=10)

        self.btn_connect = customtkinter.CTkButton(master=self, text="Disconnect", command=self.disconnect_plot)
        self.btn_connect.pack(pady=5, padx=10)

    def connect_plot(self):
        port_com = self.combo_box.get()
        self.connection = ConnectSerial(port_com, 9600)
        print('connecting...')
        try:
            self.connection.connect()
            # connect.connect()
            self.text_connect = "Connencted"
            self.user_label.configure(text=self.text_connect, text_color="Green")
            print(self.text_connect)

        except ConnectionError:
            pass

    def disconnect_plot(self):
        self.connection.disconnect()
        self.text_connect = "Disconnected"
        self.user_label.configure(text=self.text_connect, text_color="Red")

    def tap(self):
        self.connection.send_command('tap')

    def start(self):
        self.connection.send_command('start')

    def cancel(self):
        self.connection.send_command('cancel')

    def home(self):
        self.connection.send_command('home')

    def send(self):
        print("Sending!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
