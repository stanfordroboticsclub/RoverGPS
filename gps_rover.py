
"""
This script interfaces with the sparkfun GPS module in Rover mode

It publishes the rovers location to port 8860
If it receives RTCM correction on port 8290 it will also use them
"""
import serial, pynmea2, time, math
from UDPComms import Publisher, Subscriber, timeout


# pub_gps = Publisher(8280)
rtcm_sub = Subscriber(8290, timeout=0)

ser = serial.Serial("/dev/tty.usbmodem1421", timeout = 0, writeTimeout = 0)

def project(lat, lon, lat_orig, lon_orig):
    RADIUS = 6371 * 1000
    lon_per_deg = RADIUS * 2 * math.pi / 360
    lat_per_deg = lon_per_deg * math.cos(math.radians(lat_orig))

    x = (lon - lon_orig) * lon_per_deg
    y = (lat - lat_orig) * lat_per_deg

    return (x,y)


try:
    while 1:
        try:
            correction = rtcm_sub.recv()
            print("got correction")
        except:
            pass
        else:
            ser.write(correction["rtcm"])

        line = ser.readline()
        if line[0:2] == '$G':
            msg = pynmea2.parse(str(line))
            if(msg.sentence_type == "GGA"):
                print(msg.latitude, msg.longitude)
                print(repr(msg))
                # pub_gps.send( [msg.latitude, msg.longitude] )

                try:
                    print(project(msg.latitude, msg.longitude, 
                            correction['lat'], correction['lon']))
                except:
                    pass



except KeyboardInterrupt:
    print('closing')
    ser.close()
    raise
except:
    ser.close()
    raise
