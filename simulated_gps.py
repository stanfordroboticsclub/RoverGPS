
import time
from UDPComms import Publisher

# Create a UDP Publisher and set it to the correct data types
fields = "time sats lat lon alt error_lat error_lon error_alt"
format_ = "ii3f3f"
port = 8860
pub = Publisher(fields, format_, port)


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
    pub.send(0, 4, lat, lon, 0, 0, 0, 0)
    time.sleep(1)
