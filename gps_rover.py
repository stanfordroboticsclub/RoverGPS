
"""
This script interfaces with the sparkfun GPS module in Rover mode

It publishes the rovers location to port 8860
If it recives RTCM correction on port XXXX it will also use them
"""
import serial, pynmea2, time
from UDPComms import Publisher


# pub = Publisher(8860)

ser = serial.Serial("/dev/tty.usbmodem1411", timeout = 0, writeTimeout = 0)

try:
while 1:
    line = ser.readline()
    if line[0:2] == '$G':
        msg = pynmea2.parse(str(line))
        try:
            if(msg.sentence_type == "GGA"):
                print(msg.latitude, msg.longitude)
                print(repr(msg))
                print(ser.in_waiting, ser.out_waiting)
        except AttributeError:
            pass

except KeyboardInterrupt:
    print('closing')
    ser.close()
    raise
except:
    ser.close()
    raise
