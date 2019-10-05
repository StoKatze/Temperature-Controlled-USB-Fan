import time
import smbus2
import bme280
import requests
import RPi.GPIO as GPIO

# Constants
SENSOR_PORT = 1
SENSOR_ADDRESS = 0x77 # Check your address before running this script

URL = 'http://localhost:8086/write' # InfluxDB write URL
READING_DATA_PERIOD_MS = 5000.0
SENDING_PERIOD = 2
MAX_LINES_HISTORY = 1000

def main():
	try:
		# DB connection params
		dbParams = {"db": "sensori", "precision": "ms"}
	
		# Initialization
		bus = smbus2.SMBus(SENSOR_PORT)
		bme280.load_calibration_params(bus, SENSOR_ADDRESS)
	
		payload = ""
		counter = 1
		problem_counter = 0
	
		GPIO.setmode(GPIO.BOARD) # Set GPIO mode to BOARD
		PIN_IMP = 7 # Pin 7 is connected to relay
		GPIO.setup(PIN_IMP, GPIO.OUT) # Sets relay as output
	
		# Infinite loop
		while True:
			unix_time_ms = int(time.time()*1000)
		
			# Read sensor data and convert it to line protocol
			data = bme280.sample(bus, SENSOR_ADDRESS)
			line = "sensors_data temperature={},pressure={},humidity={} {}\n".format(data.temperature, data.pressure, data.humidity, unix_time_ms)
		
			payload += line
		
			# Verbose
			print("Temperature: ", data.temperature)
			print("Pressure: ", data.pressure)
			print("Humidity: ", data.humidity)
		
			if data.temperature > 25:
				GPIO.output(PIN_IMP, GPIO.HIGH) # Relay on
			elif data.temperature < 10: # Temp too low triggers relay to avoid liquid forming on the RPi
				GPIO.output(PIN_IMP, GPIO.HIGH) # Relay on
			else:
				GPIO.output(PIN_IMP, GPIO.LOW) # Realay off
		
			if counter % SENDING_PERIOD == 0:
				try:
					# Try to send data
					r = requests.post(URL, params=dbParams, data=payload)
					if r.status_code != 204:
						raise Exception("data not written")
					payload = ""
				except:
					problem_counter += 1
					print('cannot write to InfluxDB')
					if problem_counter == MAX_LINES_HISTORY:
						problem_counter = 0
					payload = ""
		
			counter += 1
		
			# Wait for selected time
			time_diff_ms = int(time.time()*1000) - unix_time_ms
			if time_diff_ms < READING_DATA_PERIOD_MS:
				time.sleep((READING_DATA_PERIOD_MS - time_diff_ms)/1000.0)
	finally:
		GPIO.cleanup() # Frees GPIO pins
		
if __name__ == "__main__":
	main()
