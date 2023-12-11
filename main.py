import sys
import tkinter
import math
import customtkinter
from connect_serial import *
import serial.tools.list_ports


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self._set_appearance_mode("Dark")
        self.O1X = 35.0
        self.O1Y = -40.0
        self.O2X = 80.0
        self.O2Y = -40.0
        self.L1 = 50.0
        self.L2 = 90.0
        self.servofaktorLeft_default = 0.95  # adjust the following factor until the servos move exactly 90 degrees
        self.servofaktorRight_default = 0.90  # adjust the following factor until the servos move exactly 90 degrees
        self.servofaktorLeft = self.servofaktorLeft_default
        self.servofaktorRight = self.servofaktorRight_default
        self.M_PI = math.pi
        self.servoLeftNull = 180  # to adjust the NULL-values so that the servo arms are at all times parallel?
        self.servoRightNull = 180  # adjust the NULL-values so that the servo arms are at all times parallel?
        self.list_port = []
        self.text_connect = "Disconnected"

        self.radio_var = tkinter.IntVar()
        self.connection = None
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.title("Plot_C Control GUI")
        self.geometry("700x540")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # ====================== sidebar =========================================
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # logo_label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PLOT_C GUI", font=customtkinter.CTkFont(size=20, weight="bold"))
        # label text
        self.user_label = customtkinter.CTkLabel(master=self.sidebar_frame, text=self.text_connect, text_color="Red", pady=50)
        # btn connect
        self.btn_connect = customtkinter.CTkButton(master=self.sidebar_frame, text="Connect", command=self.connect_plot)

        self.combo_box = customtkinter.CTkComboBox(master=self.sidebar_frame,
                                                   values=[],
                                                   )
        self.check_list_of_ports()
        self.btn_refresh_port = customtkinter.CTkButton(master=self.sidebar_frame, text="Refresh COM port", command=self.check_list_of_ports)
        self.btn_disconnect = customtkinter.CTkButton(master=self.sidebar_frame, text="Disconnect", command=self.disconnect_plot)

        self.btn_disconnect.configure(state="disabled")
        # layouts of buttons
        self.logo_label.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        self.user_label.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")
        self.btn_connect.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="n")
        self.combo_box.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="n")
        self.btn_refresh_port.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="n")
        self.btn_disconnect.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="n")
        # =====================/ sidebar =========================================

        # ========================= coordinate_box =========================================
        self.tab_view = customtkinter.CTkTabview(self, width=300)
        self.tab_view.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tab_view.add("Set X and Y")
        self.tab_view.add("Pre-defined position")
        self.tab_view.add("Programs")
        self.tab_view.add("Calibrations")
        # =================================== tab Set X and Y ===========================================
        self.set_x_cor = customtkinter.CTkEntry(master=self.tab_view.tab('Set X and Y'), placeholder_text="Set x pos")
        self.set_y_cor = customtkinter.CTkEntry(master=self.tab_view.tab('Set X and Y'), placeholder_text="Set y pos")
        self.label_set_a1 = customtkinter.CTkLabel(master=self.tab_view.tab('Set X and Y'), text="Set X position on screen", text_color="White", pady=5)
        self.label_set_a2 = customtkinter.CTkLabel(master=self.tab_view.tab('Set X and Y'), text="Set Y position on screen", text_color="White", pady=5)
        self.btn_coordinates = customtkinter.CTkButton(master=self.tab_view.tab('Set X and Y'), text="Set coordinates", command=self.set_XY)
        self.radiobutton_1 = customtkinter.CTkRadioButton(master=self.tab_view.tab('Set X and Y'),
                                                          text="Lift Finger",
                                                          variable=self.radio_var,
                                                          value=1,
                                                          radiobutton_width=20,
                                                          border_width_unchecked=2,
                                                          border_width_checked=5,
                                                          fg_color='red')
        self.radiobutton_2 = customtkinter.CTkRadioButton(master=self.tab_view.tab('Set X and Y'),
                                                          text="Push Finger",
                                                          variable=self.radio_var,
                                                          value=0,
                                                          radiobutton_width=20,
                                                          border_width_unchecked=2,
                                                          border_width_checked=5,
                                                          fg_color='red')
        self.radiobutton_3 = customtkinter.CTkRadioButton(master=self.tab_view.tab('Set X and Y'),
                                                          text="Tap Finger", variable=self.radio_var,
                                                          value=10,
                                                          radiobutton_width=20,
                                                          border_width_unchecked=2,
                                                          border_width_checked=5,
                                                          fg_color='red')

        self.set_x_cor.grid(row=0, column=1, padx=(10, 10), pady=(20, 10))
        self.set_y_cor.grid(row=1, column=1, padx=(10, 10), pady=(20, 10))
        self.label_set_a1.grid(row=0, column=0, padx=(10, 10), pady=(20, 10))
        self.label_set_a2.grid(row=1, column=0, padx=(10, 10), pady=(20, 10))
        self.btn_coordinates.grid(row=2, column=0, padx=(10, 10), pady=(20, 10))
        self.radiobutton_1.grid(row=0, column=2, padx=(10, 10), pady=(20, 10))
        self.radiobutton_2.grid(row=1, column=2, padx=(10, 10), pady=(20, 10))
        self.radiobutton_3.grid(row=2, column=2, padx=(10, 10), pady=(20, 10))
        # =================================== tab Calibrations ===========================================
        self.set_x_cor_cal = customtkinter.CTkEntry(master=self.tab_view.tab('Calibrations'), placeholder_text="Set x pos")
        self.set_y_cor_cal = customtkinter.CTkEntry(master=self.tab_view.tab('Calibrations'), placeholder_text="Set y pos")
        self.btn_coordinates = customtkinter.CTkButton(master=self.tab_view.tab('Calibrations'), text="Set coordinates", command=self.set_XY)
        self.set_faktor_1 = customtkinter.CTkEntry(master=self.tab_view.tab('Calibrations'), placeholder_text="Set faktor 1")
        self.set_faktor_2 = customtkinter.CTkEntry(master=self.tab_view.tab('Calibrations'), placeholder_text="Set faktor 2")
        calibration_text = 'After you find faktor values\n you need to change it in code directly. \n\nThis program is still under development'
        self.label_description = customtkinter.CTkLabel(master=self.tab_view.tab('Calibrations'),
                                                        text=calibration_text, text_color="White", pady=5)
        self.set_x_cor_cal.grid(row=0, column=0, padx=(10, 10), pady=(20, 10))
        self.set_y_cor_cal.grid(row=1, column=0, padx=(10, 10), pady=(20, 10))
        self.set_faktor_1.grid(row=0, column=1, padx=(10, 10), pady=(20, 10))
        self.set_faktor_2.grid(row=1, column=1, padx=(10, 10), pady=(20, 10))
        self.btn_coordinates.grid(row=2, column=0, padx=(10, 10), pady=(20, 10))
        self.label_description.grid(row=(3), columnspan=(2), padx=(10, 10), pady=(20, 10))

        # ========================= /coordinate_box =======================================
        # radiobutton_1 = customtkinter.CTkRadioButton(master=self, text="Lift Finger", variable=self.radio_var, value=1, radiobutton_width=30, border_width_unchecked=2, border_width_checked=5,
        #                                              fg_color='red')
        # radiobutton_2 = customtkinter.CTkRadioButton(master=self, text="Push Finger", variable=self.radio_var, value=0, radiobutton_width=30, border_width_unchecked=2, border_width_checked=5,
        #                                              fg_color='red')
        # radiobutton_3 = customtkinter.CTkRadioButton(master=self, text="Tap Finger", variable=self.radio_var, value=10, radiobutton_width=30, border_width_unchecked=2, border_width_checked=5,
        #                                              fg_color='red')
        #
        # # radiobutton_1.pack(padx=20, pady=10)
        # radiobutton_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        # radiobutton_2.pack(padx=20, pady=10)
        # radiobutton_3.pack(padx=20, pady=10)
        #
        # self.btn_connect = customtkinter.CTkButton(master=self, text="Set angle", command=self.send)
        # self.btn_connect.pack(pady=20)
        #
        # input faktor and servonull
        # self.set_faktor_1 = customtkinter.CTkEntry(master=self, placeholder_text="Set faktor 1")
        # self.set_faktor_2 = customtkinter.CTkEntry(master=self, placeholder_text="Set faktor 2")
        # self.set_faktor_1.pack(pady=20, padx=4)
        # self.set_faktor_2.pack(pady=8, padx=4)
        #
        # # input x and y
        # self.user_label_x = customtkinter.CTkLabel(master=self, text="set X", text_color="green", pady=2)
        # self.set_x = customtkinter.CTkEntry(master=self, placeholder_text="Set x point")
        # self.user_label_y = customtkinter.CTkLabel(master=self, text="set Y", text_color="green", pady=2)
        # self.set_y = customtkinter.CTkEntry(master=self, placeholder_text="Set y point")
        # self.btn_connect = customtkinter.CTkButton(master=self, text="Set coordinates", command=self.set_XY)
        # self.user_label_x.pack()
        # self.set_x.pack(pady=20, padx=4)
        # self.user_label_y.pack()
        # self.set_y.pack(pady=8, padx=4)
        # self.btn_connect.pack(pady=20)
        #
        # self.user_label = customtkinter.CTkLabel(master=self, text=self.text_connect, text_color="Red", pady=50)
        # self.user_label.pack()
        #
        # self.btn_connect = customtkinter.CTkButton(master=self, text="Tap", command=self.tap)
        # # self.btn_connect.pack(pady=5, padx=10)
        # self.btn_connect = customtkinter.CTkButton(master=self, text="Start", command=self.start)
        # # self.btn_connect.pack(pady=5, padx=10)
        # self.btn_connect = customtkinter.CTkButton(master=self, text="Cancel", command=self.cancel)
        # # self.btn_connect.pack(pady=5, padx=10)
        # self.btn_connect = customtkinter.CTkButton(master=self, text="Home", command=self.home)
        # # self.btn_connect.pack(pady=5, padx=10)
        #
        # self.btn_connect = customtkinter.CTkButton(master=self, text="Connect", command=self.connect_plot)
        # self.btn_connect.pack(ipady=30, padx=10, pady=30)

        # region port list
        # self.get_port = serial.tools.list_ports.comports()
        # list_port = []
        # for port, desc, hwid in sorted(self.get_port):
        #     print(port, desc, hwid)
        #     if "CH340" in desc:
        #         list_port.append(port)
        # self.combo_box = customtkinter.CTkComboBox(master=self,
        #                                            values=list_port)
        # self.combo_box.pack(pady=5, padx=10)
        # endregion

        # self.btn_connect = customtkinter.CTkButton(master=self, text="Disconnect", command=self.disconnect_plot)
        # self.btn_connect.pack(pady=5, padx=10)
        #

        self.Point_X = self.set_x_cor.get()
        self.Point_Y = self.set_y_cor.get()

    def check_list_of_ports(self):

        self.get_port = serial.tools.list_ports.comports()
        self.list_port = []
        for port, desc, hwid in sorted(self.get_port):
            print(port, desc, hwid)
            if "CH340" in desc:
                self.list_port.append(port)
        if len(self.list_port) == 0:
            self.user_label.configure(text='No devices found.', text_color="Yellow")
            self.combo_box.set('')
            self.btn_connect.configure(state='disabled')
        else:
            self.combo_box.set('')
            self.user_label.configure(text='Device found\nCheck port box below', text_color="Orange")
            self.btn_connect.configure(state='Enabled')
            self.combo_box.configure(values=self.list_port)

    def connect_plot(self):
        port_com = self.combo_box.get()
        self.connection = ConnectSerial(port_com, 9600)
        print('connecting...')
        try:
            self.connection.connect()
            # connect.connect()
            self.text_connect = "Connected"
            self.user_label.configure(text=self.text_connect, text_color="Green")
            self.btn_connect.configure(state="disabled")
            self.btn_disconnect.configure(state="enabled")
            self.btn_refresh_port.configure(state="disabled")
            print(self.text_connect)

        except:
            self.user_label.configure(text='Connection Error\n Check if device is plugged in', text_color="Yellow")
            pass

    def disconnect_plot(self):
        self.connection.disconnect()
        self.text_connect = "Disconnected"
        self.user_label.configure(text=self.text_connect, text_color="Red")
        self.btn_connect.configure(state="enabled")
        self.btn_disconnect.configure(state="disabled")
        self.btn_refresh_port.configure(state="enabled")
        print(self.text_connect)

    def tap(self):
        # self.connection.send_command('tap')
        pass

    def start(self):
        # self.connection.send_command('start')
        self.connection.send_bytes_s(f'x{160}y0{90}')

    def cancel(self):
        self.connection.send_command('cancel')

    def home(self):
        self.connection.send_command('home')

    def send(self):
        print("Sending!")

        x = self.set_x_cor.get()
        if 10 < int(x) < 100:
            x = f'0{x}'
        elif int(x) > 180:
            x = f'180'
        elif int(x) < 10:
            x = f'00{x}'

        y = self.set_y_cor.get()
        if 10 < int(y) < 100:
            y = f'0{y}'
        elif int(y) > 180:
            y = f'180'
        elif int(y) < 10:
            y = f'00{y}'

        self.connection.send_bytes_s(f'x{x}y{y}z{self.radio_var.get()}')

    def set_XY(self):

        print(f"Debug == [{self.servofaktorLeft}].left and [{self.servofaktorRight}].right")

        self.Point_X = self.set_x_cor.get()
        self.Point_Y = self.set_y_cor.get()
        if self.set_faktor_1.get() != "":
            self.servofaktorRight = float(self.set_faktor_1.get())  # for x
        else:
            self.servofaktorRight = self.servofaktorRight_default  # for x

        if self.set_faktor_2.get() != "":
            self.servofaktorLeft = float(self.set_faktor_2.get())  # for y
        else:
            self.servofaktorLeft = self.servofaktorLeft_default  # for x

        print(f'Debug == [{self.set_faktor_1.get()}].faktor1 [{self.set_faktor_2.get()}].faktor2')
        print(f'Debug == [{self.Point_X}].POINT_X and [{self.Point_Y}].POINT_Y')

        dx = int(self.Point_X) - self.O1X
        dy = int(self.Point_Y) - self.O1Y
        c = math.sqrt(dx ** 2 + dy ** 2)
        a1 = math.atan2(dy, dx)
        a2 = App.return_angle(self.L1, self.L2, c)
        x = (a2 + a1) * self.servofaktorRight

        # =================== a1 angle calculated and ready to write ===========================

        # region debug prints
        # print(f"Debug == [{dx}].dx")
        # print(f"Debug == [{dy}].dy")
        # polar length c and angle a1
        # print(f"Debug == [{c}].c")
        # print(f"Debug == [{a1}].a1")
        # print(f"Debug == [{a2}].a2 from return angle")
        # calculate position for servo left
        # print(f'Debug == calculated x [{x}].x')

        # print(f"Debug == [{a2}].a2 from return angle")
        # calculate position for servo right
        # print(f'Debug == calculated y [{y}].y')
        # endregion

        dx = int(self.Point_X) - self.O2X
        dy = int(self.Point_Y) - self.O2Y
        c = math.sqrt(dx ** 2 + dy ** 2)
        a1 = math.atan2(dy, dx)
        a2 = App.return_angle(self.L1, self.L2, c)
        # y = (((a1 - a2) * self.servofaktorLeft) + self.servoRightNull)
        y = (a1 - a2) * self.servofaktorLeft
        print(f"Debug ")
        #
        x = self.servoRightNull - (x * 180) / self.M_PI + 90
        y = self.servoLeftNull - (y * 180) / self.M_PI - 90

        print(f'Debug == [{self.servoRightNull}].servRightNull')
        print(f'Debug == [{self.servoLeftNull}].servLeftNull')

        print(f' a1 angle is [{x}].angle_X')
        print(f' a2 angle is [{y}].angle_Y')

        self.connection.send_bytes_s(f'x{round(x)}y{round(y)}z{int(self.radio_var.get())}')

    @staticmethod
    def return_angle(a, b, c):
        acos_m = 0
        calc_acos = (a * a + c * c - b * b) / (2 * a * c)
        print(f'Debug == [{calc_acos}].calc_acos = {a, b, c}')
        try:
            acos_m = math.acos(calc_acos)
        except:
            print('! Can\'t calculate')

        return acos_m


if __name__ == "__main__":
    app = App()
    app.mainloop()
