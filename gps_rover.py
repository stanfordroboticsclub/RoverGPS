
"""
This script interfaces with the sparkfun GPS module in Rover mode

It publishes the rovers location to port 8280
If it receives RTCM correction on port 8290 it will also use them
"""
import time, math, datetime
import serial, pynmea2
from UDPComms import Publisher, Subscriber, timeout


pub_gps = Publisher(8280)
rtcm_sub = Subscriber(8290, timeout=0)

ser = serial.Serial("/dev/serial0", timeout = None, writeTimeout = 0)

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
        #print line
        if line[0:2] == '$G':
            msg = pynmea2.parse(str(line))
            if(msg.sentence_type == "GGA"):
                print(msg.latitude, msg.longitude)
                print(repr(msg))

                #print(msg.timestamp)
                #timestamp = (msg.timestamp - datetime(1970, 1, 1)).total_seconds()
                # TODO
                timestamp = 0

                try:
                    x,y = project(msg.latitude, msg.longitude, 
                            correction['lat'], correction['lon'])
                    local = [ True, x, y]
                except:
                    local = [ False, 0 ,0]

                to_send = { "time": timestamp,
                            "lat": msg.latitude,
                            "lon": msg.longitude,
                            "alt": msg.altitude,
                            "sats": msg.num_sats,
                            "qual": msg.gps_qual,
                            "age": msg.age_gps_data,
                            "local":local}
                            
                pub_gps.send(to_send)



except KeyboardInterrupt:
    print('closing')
    ser.close()
    raise
except:
    ser.close()
    raise
