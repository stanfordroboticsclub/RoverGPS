

from httplib import HTTPConnection
from base64 import b64encode

import serial, pynmea2, time
from user_pass import user

publish_interval = 1

pub = Publisher(8290)

server ="rtgpsout.unavco.org:2101"

headers = {
    'Ntrip-Version': 'Ntrip/2.0',
    'User-Agent': 'NTRIP ntrip_ros',
    'Connection': 'close',
    'Authorization': 'Basic ' + b64encode(user)
}

connection = HTTPConnection(server)
connection.request('GET', '/SLAC_RTCM3',body=None, headers=headers)
response = connection.getresponse()

# Message format
# https://forum.u-blox.com/index.php/16898/decoding-rtcm3-message
def get_length(msg):
    assert( msg[0] == chr(0xd3))
    return (ord(msg[1])* 8 + ord(msg[2])) & 0x3ff

buf = ""
msgs = []


last_message = time.time()

while 1:
    if response.isclosed():
        print "responce closed"
        break
    buf += response.read(100)
    length = get_length(buf)
    next_header = buf[length:].find( chr(0xd3) )
    # print(length,next_header, len(buf), len(msgs))
    # print buf[length: length + next_header].encode("hex")
    if (next_header == -1):
        print "no header found"
        continue
    msgs.append( buf[:length + next_header ] )
    buf = buf[length + next_header:]

    if (time.time() - last_message) > publish_interval:
        rtcm = "".join(msgs)
        print(len("".join(msgs)))
        msgs = []
        last_message = time.time()

        # timestamp = (msg.timestamp - datetime(1970, 1, 1)).total_seconds()
        to_send = { "time": 0,
                    "lat": 0,
                    "lon": 0,
                    "alt": 0,
                    "sats": 0,
                    "rtcm": rtcm}

        pub.send(to_send)






