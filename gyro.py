#!/usr/bin/env python3

import time
import serial
from UDPComms import Publisher

fields = "angle"
format_ = "f"
port = 8870
pub = Publisher(fields, format_, port)

uart = serial.Serial("/dev/ttyUSB1", baudrate=115200, timeout=3000)

last_print = time.monotonic()
while True:
    current = time.monotonic()
    angle = float(uart.readline()[7:])

    if current - last_print >= 0.1:
        print(angle)
        last_print = current
        pub.send(angle)


