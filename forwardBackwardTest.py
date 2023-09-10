import serial
import time

# Establish the serial connection
arduino = serial.Serial('/dev/ttyUSB0', 9600)  
time.sleep(2)  # Wait for the serial connection to initialize

arduino.write(b'F')  # Send the letter 'F' to the Arduino
time.sleep(2)  # Wait for 2 seconds

arduino.write(b'B')  # Send the letter 'S' to the Arduino

time.sleep(2)  # Wait for 2 seconds

arduino.close()
