#!/usr/bin/env python3

from UDPComms import Publisher
import time
from Adafruit_BNO055 import BNO055
import json
 
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
pub = Publisher(8220)


if not bno.begin(BNO055.OPERATION_MODE_NDOF):
#if not bno.begin(BNO055.OPERATION_MODE_COMPASS):
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

#with open('BNO_calibration.json','r') as f:
    #calibration = json.load(f)
    #bno.set_calibration(calibration)

while True:
    to_send = {"temp": bno.read_temp(),
               "angle": bno.read_euler(),
               "gravity": bno.read_gravity(),
               "accel": bno.read_linear_acceleration(),
               "calibration": bno.get_calibration_status()}

    pub.send(to_send)
    #print(bno.read_magnetometer(), bno.read_gyroscope(),  to_send)
    print(to_send)
 
    time.sleep(0.05)
