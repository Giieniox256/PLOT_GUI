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
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

