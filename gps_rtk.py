
from httplib import HTTPConnection
from base64 import b64encode

import serial, pynmea2, time

server ="rtgpsout.unavco.org:2101"

headers = {
    'Ntrip-Version': 'Ntrip/2.0',
    'User-Agent': 'NTRIP ntrip_ros',
    'Connection': 'close',
    'Authorization': 'Basic ' + b64encode(user)
}
ser= serial.Serial("/dev/ttyACM0", timeout = 0, writeTimeout = 0)
connection = HTTPConnection(server)
connection.request('GET', '/SLAC_RTCM3',body=None, headers=headers)
response = connection.getresponse()
last_time = time.time()


buf = ""
try:
    while 1:
        buf += ser.read(100)
        if buf.find("\n") != -1:
            pos = buf.find("\n")
            line = buf.split("\n",1)
            buf = line[1]
            line = line[0]
        else:
            # print(len(buf))
            continue

        #line = ser.readline()

        #data = response.read(100)
        #pos = data.find('\r\n')
        #if pos != -1:
            #correction = buf + data[:pos]
            #buf = data[pos+2:]
            #ser.write(correction)
        #else: buf += data
        if response.isclosed():
            print("dead")
            exit()


        if line[0:2] == b'$G':
            if (time.time() - last_time) > 1:
                print("write rtcm")
                #connection = HTTPConnection(server)
                #connection.request('GET', '/SLAC_RTCM3',body=None, headers=headers)
                #response = connection.getresponse()
                #if response.status != 200: raise Exception("blah")
                print()
                ser.write(response.read(500))
                last_time = time.time()

            msg = pynmea2.parse(str(line))
            try:
                if(msg.sentence_type == "GGA"):
                    print(msg.latitude, msg.longitude)
                    print(repr(msg))
                    print( ser.in_waiting, ser.out_waiting)
            except AttributeError:
                pass
except KeyboardInterrupt:
    print('closing')
    ser.close()
    raise
except:
    ser.close()
    raise
