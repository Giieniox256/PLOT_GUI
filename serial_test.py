import time

import serial

def test():
    ser = serial.Serial()

    ser.baudrate = 9600
    ser.stopbits = 1
    ser.bytesize = 8
    ser.parity = 'N'
    ser.port = 'COM12'
    ser.open()
    time.sleep(1)
    ser.write(b'tap\n')
    time.sleep(3)
    ser.write(b'start')
    time.sleep(3)
    ser.write(b'cancel')
    time.sleep(3)
    ser.write('start'.encode())
    ser.close()

import math

def set_XY(Tx, Ty):
    dx, dy, c, a1, a2, Hx, Hy = 0, 0, 0, 0, 0, 0, 0

    # calculate triangle between pen, servoLeft and arm joint
    # cartesian dx/dy
    dx = Tx - O1X
    dy = Ty - O1Y

    # polar lemgth (c) and angle (a1)
    c = math.sqrt(dx * dx + dy * dy)
    a1 = math.atan2(dy, dx)
    a2 = return_angle(L1, L2, c)

    servo2.writeMicroseconds(math.floor(((a2 + a1 - math.pi) * SERVOFAKTORLEFT) + SERVOLEFTNULL))

    # calculate join arm point for triangle of the right servo arm
    a2 = return_angle(L2, L1, c)
    Hx = Tx + L3 * math.cos((a1 - a2 + 0.621) + math.pi) #36,5°
    Hy = Ty + L3 * math.sin((a1 - a2 + 0.621) + math.pi)

    # calculate triangle between pen joint, servoRight and arm joint
    dx = Hx - O2X
    dy = Hy - O2Y

    c = math.sqrt(dx * dx + dy * dy)
    a1 = math.atan2(dy, dx)
    a2 = return_angle(L1, (L2 - L3), c)

    servo3.writeMicroseconds(math.floor(((a1 - a2) * SERVOFAKTORRIGHT) + SERVORIGHTNULL))


if __name__ == '__main__':
    test()