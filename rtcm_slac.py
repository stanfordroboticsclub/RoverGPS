

from httplib import HTTPConnection
from base64 import b64encode

import serial, pynmea2, time
from user_pass import user

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

def get_length(msg):
    assert( msg[0] == chr(0xd3))
    return (ord(msg[1])* 8 + ord(msg[2])) & 0x3ff

buf = ""
msgs = []

while 1:
    buf += response.read(100)
    print(len(buf), len(msgs))
    length = get_length(buf)
    next_header = buf[length:].find( chr(0xd3) )
    if (next_header == -1):
        print "no header found"
        continue
    msgs.append( buf[:length + next_header ] )
    buf = buf[length + next_header:]




