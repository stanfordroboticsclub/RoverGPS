#!/usr/bin/env sh

FOLDER=$(dirname $(realpath "$0"))
cd $FOLDER

yes | pip3 install adafruit-circuitpython-gps
yes | pip3 install adafruit-circuitpython-bno055
yes | pip install pynmea2
yes | pip install pyserial

for file in *.service; do
    [ -f "$file" ] || break
    sudo ln -s $FOLDER/$file /lib/systemd/system/
done

sudo systemctl daemon-reload
echo "make sure the enable i2c and clock streching!!"
