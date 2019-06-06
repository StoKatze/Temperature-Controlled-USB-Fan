# Temperature-Controlled-USB-Fan
A BME280 temperature sensor triggers a relay that turns on a fan and also sends temperature, pressure and humidity data to an Influx DB server. The data is then available through Grafana. 

## Requirements
##### Software
* Python 3 (Should be installed by default on Raspbian - [How to install](https://www.raspberrypi.org/forums/viewtopic.php?t=181480)) 
* Python 3 smbus2 package ```sudo pip3 install smbus2```
* Python 3 bme280 package ```sudo pip3 install bme280```
* Python 3 RPi.GPIO package ```sudo pip3 install RPi.GPIO```
* InfluxDB - [Instructions (should work fine on Raspbian Stretch too)](https://gist.github.com/boseji/bb71910d43283a1b84ab200bcce43c26)
* Grafana - ```wget https://dl.grafana.com/oss/release/grafana-rpi_6.2.1_armhf.deb && sudo dpkg -i grafana-rpi_6.2.1_armhf.deb ``` - [Grafana website](https://grafana.com/grafana/download?platform=arm)
               
##### Hardware
* Raspberry Pi
* BME280 Sensor
* 1 Channel 5V Relay [(Something like this)](https://www.amazon.com/dp/B00VRUAHLE/)
* 5V fan
* If you plan on using a 5V USB fan you also need a USB female to motherboard header [(something like this)](https://www.amazon.com/StarTech-Motherboard-4-Pin-Header-USBMBADAPT/dp/B000IV6S9S)
* Breadboard

## Wiring scheme
*very soon*

## Usage 
*soon*

