#!/usr/bin/env sh

FOLDER=$(dirname $(realpath "$0"))
cd $FOLDER

yes | pip install pyserial
yes | pip3 install adafruit-circuitpython-gps
yes | pip3 install Adafruit-BNO055
yes | pip install pynmea2

for file in *.service; do
    [ -f "$file" ] || break
    sudo ln -s $FOLDER/$file /lib/systemd/system/
done

sudo systemctl daemon-reload

#yes | pip3 install adafruit-circuitpython-bno055
#echo "make sure the enable i2c and clock streching!!"
