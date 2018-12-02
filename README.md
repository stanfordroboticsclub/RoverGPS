# RoverGPS
Publishes the rover's GPS location to the UDP network

- `gps.service` - Connects to Adafuit GPS on `/dev/ttyUSB0` and publishes coordinates. Sometimes there is an issue where there is no light on the GPS board after the script is turned on and it needs to be power cycled by unplugging and replugging the VIN jumper.

- `gyro.service` - Connects to the 2017 sensor board on `/dev/ttyUSB1` and publishes gyro Z measurement

- `simulated_gps.py` - publishes fake GPS coordinates around the Stanford campus so you can test the GUI without a real GPS signal (eg inside a building). Don't forget to turn off `gps.service` as they will conflict.
 
Caveats
-------

- Make sure the GPS is connected as `/dev/ttyUSB0` and the gyro is connected as `/dev/ttyUSB1`. This can be accomplished by plugging in the GPS before the gyro

- Sometime the adafruit GPS requires a restart after power on if the LED is off. You can do this by unplugging and replugging the brown wire (going from the GPS to the GPS)
