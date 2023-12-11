import time

import serial

class ConnectSerial:
    def __init__(self, port, baudrate):
        self.serial_p = serial.Serial()
        self.port = port
        self.baudrate = baudrate

    def connect(self):
        self.serial_p = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.5
        )

    def disconnect(self):
        self.serial_p.close()

    def send_command(self, command: str):
        self.serial_p.write(command.encode())
        # self.serial_p.send_break()
        print(command.encode())
        # print(self.serial_p.read())

    def send_bytes_s(self, data):
        self.serial_p.write(data.encode())
        print(data)
        print("Encoded", data.encode())
