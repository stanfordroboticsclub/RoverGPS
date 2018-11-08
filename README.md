# RoverGPS
Publishes the rover's GPS location to the UDP network

`gps.service` - Connects to Adafuit GPS on `/dev/ttyUSB0` and publishes coordinates. Sometimes there is an issue where there is no light on the GPS board after the script is turned on and it needs to be power cycled by unplugging and repluggin the VIN jumper.

`gyro.service` - Connects to the 2017 sensor board on `/dev/ttyUSB1` and publishes gyro Z measument

`simulated_gps.py` - publishes fake GPS coordiantes around the Stanford campus so you can test the GUI without a real GPS signal (eg inside a building). Don't forget to turn off `gps.service` as they will conflict.
 