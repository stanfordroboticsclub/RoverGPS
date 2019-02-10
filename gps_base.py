
"""
This script interfaces with the sparkfun GPS module in Base station mode

It publishes RTCM corrections on port 8290 for the rover to use
"""
import serial, pynmea2, time
from UDPComms import Publisher


pub = Publisher(8290)
ser = serial.Serial("/dev/ttyS0", timeout = 0, writeTimeout = 0)

# Message format
# https://forum.u-blox.com/index.php/16898/decoding-rtcm3-message
def get_length(msg):
    assert( msg[0] == chr(0xd3))
    return (ord(msg[1])* 8 + ord(msg[2])) & 0x3ff

rtcm_stream = []

try:
    while 1:
        line = ser.readline()
        if line == "":
            continue
        if line[0:2] == b'$G':
            msg = pynmea2.parse(str(line))
            if(msg.sentence_type == "GGA"):
                print(repr(msg))
                rtcm = b''.join(rtcm_stream)
                print(ser.in_waiting, ser.out_waiting, len(rtcm))
                rtcm_stream = []

                timestamp = (msg.timestamp - datetime(1970, 1, 1)).total_seconds()
                to_send = { "time": timestamp,
                            "lat": msg.latitude,
                            "lon": msg.longitude,
                            "alt": msg.altitude,
                            "sats": msg.num_sats,
                            "rtcm": rtcm}

                pub.send(to_send)

        else:
            rtcm_stream.append(line)
        # elif line[0] == chr(0xd3):
        #     length = get_length(line)
        #     print("RTCM", length, len(line) , len(line) - length) 

        # else:
        #     print("unknown", len(line))

except KeyboardInterrupt:
    print('closing')
    ser.close()
    raise
except:
    ser.close()
    raise
