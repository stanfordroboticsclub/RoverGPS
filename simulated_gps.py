
import time
from UDPComms import Publisher

# Create a UDP Publisher and set it to the correct data types

pub = Publisher(8280)

i = 0
points = [ (37.429, -122.170),
           (37.428, -122.171),
           (37.427, -122.172),
           (37.428, -122.169),
           (37.429, -122.172) ]

while True:
    lat,lon = points[i]
    print lat, lon

    i = (i+1) % len(points)

    to_send = { "time": 0,
            "lat": lat,
            "lon": lon,
            "alt": 0,
            "sats": 12,
            "qual": 5,
            "age": 1,
            "local":[False, 0, 0]}

    pub.send(to_send)
    time.sleep(1)
