# Temperature-Controlled-USB-Fan
A BME280 temperature sensor triggers a relay that turns on a fan and also sends temperature, pressure and humidity data to an Influx DB server. The data is then available through Grafana. 

## Requirements
### Software
* Python 3 (Should be installed by default on Raspbian - [How to install](https://www.raspberrypi.org/forums/viewtopic.php?t=181480)) 
* Python 3 smbus2 package ```sudo pip3 install smbus2```
* Python 3 bme280 package ```sudo pip3 install bme280```
* Python 3 RPi.GPIO package ```sudo pip3 install RPi.GPIO```
* InfluxDB - [Instructions (should work fine on Raspbian Stretch too)](https://gist.github.com/boseji/bb71910d43283a1b84ab200bcce43c26)
* Grafana - ```wget https://dl.grafana.com/oss/release/grafana-rpi_6.2.1_armhf.deb && sudo dpkg -i grafana-rpi_6.2.1_armhf.deb ``` - [Grafana website](https://grafana.com/grafana/download?platform=arm)
               
### Hardware
* Raspberry Pi
* BME280 Sensor
* 1 Channel 5V Relay [(Something like this)](https://www.amazon.com/dp/B00VRUAHLE/)
* 5V fan
* If you plan on using a 5V USB fan you also need a USB female to motherboard header [(something like this)](https://www.amazon.com/StarTech-Motherboard-4-Pin-Header-USBMBADAPT/dp/B000IV6S9S)
* Breadboard

## Wiring scheme
![Wiring scheme](https://github.com/StoKatze/Temperature-Controlled-USB-Fan/blob/master/Wiring%20Scheme/Schemaventola.png)

Wiring is fairly straight-forward. 

### General
1. Connect PIN 2 (5V) and PIN 6 (GND) to two of the breadboard's power rails
1. Connect USB VCC to 5V power rail
1. Connect USB GND to opposite GND power rail (not the one you connected the wires in the first step)

### BME280
1. 3.3V - PIN 1
1. GND - you can use the main one on the breadboard (not the one that goes to the USB plug)
1. SDA - PIN 3
1. SCL - PIN 5

### Relay
1. Connect PIN7 to any wiring rail and from there to the SIGNAL PIN on the relay (you can also use a direct connection)
1. Connect + PIN on the relay to 5V power rail
1. Connect - PIN on the relay to GND power rail
1. Connect NO to the power rail you used for USB GND
1. Connect COM to the GND power rail
1. Connect NC to any unused wiring rail

### LEDs
#### Red
1. Connect the anode of the LED to the wire coming out of NC
1. Use a 220Ω resistor (150Ω or 100Ω are fine too) to avoid frying the LED. Connect one side to the cathode and the other on the 5V power rail

#### Green
1. Connect the anode of the LED to the secondary GND power rail (the one used for USB GND)
1. Use a 220Ω resistor (150Ω or 100Ω are fine too) to avoid frying the LED. Connect one side to the cathode and the other on the 5V power rail

## Usage 
You simply need to create a new InfluxDB database, run the python script and configure Grafana.

### Check your sensor's address
1. Enable I2C via ```sudo raspi-config``` - Interfacing options > I2C > Yes > Reboot if needed
1. Use the command ```i2cdetect -y 1``` - You should see a number, usually 77 or 76 for this sensor
1. If you don't have i2cdetect install i2c-tools ```sudo apt-get update && sudo apt-get install i2c-tools``` 
1. If your sensor doesn't show up check your connections. If it still doesn't show up you might have a dead sensor

### Congfiguring InfluxDB
1. Point your browser to http://<your-raspberrypi-ip>:8083 
1. Create a new database ```CREATE DATABASE “choose-a-db-name"```

### Running the script
1. Download [sensor.py](Python/sensor.py)
1. Edit it using nano or any other text editor ```nano sensor.py```
1. Change your sensor address in line 9
1. Change your database name in line 19
1. Save and exit
1. Execute the script ```python3 sensor.py```
1. The script should print temperature, pressure and humidity values
1. OPTIONAL: you can run it to save a log file ```python3 sensor.py >> SomeFile.txt``` - You can also use screen to hide the output (```sudo apt-get update && sudo apt-get install screen && screen``` press enter and write your command. You can use ```CTRL+A+D``` to detach from your screen session and ```screen -r``` to resume it)

### Creating a Grafana dashboard
1. Point your browser to http://<your-raspberrypi-ip>:3000 - default user admin/admin - you will be asked to set a new password
1. Click on "Add Data Source", then on "Influx DB" and finally write your database name
1. Click on "Save and Test" to test your configuration and save it
1. Click on the "+" icon in the left menu and choose "Dashobard"
1. You can add a graph or any other element by using the "Add Element" button in the top right corner of the web page
1. Hover your mouse on the ghrap's title and choose "Edit":
* In the "General" tab you can change the title
* In the "Metrics" tab you can change the data shown by the graph:
  * Select Influx DB as Data Source
  * Click on the "select measurement" field in the query and choose sensors_data
  * Click on the "field(value)" field in the query and choose the data you want to show - You can choose between temperature, pessure and humidity
* In the "Axes" tab you can change the measurement unit - data will be converted automatically
* In the "Legend" tab you can hide or show the legend
* In the "Display" tab you can define how data will be shown
7. Repeat from 5 for every measurement
8. Profit!
  
## Thank you
I originally made this project to cool down my ADSB fan but some of my friends were interested so I uploaded all needed stuff here and wrote this how-to guide.
I don't know much about electronics so I tried making this circuit as easy as possible. Suggestions are welcome.
