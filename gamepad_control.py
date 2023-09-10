import serial
from evdev import InputDevice, categorize, ecodes

# Setup serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Set up the gamepad device
gamepad = InputDevice('/dev/input/event2')

# Initial command to 'Stop'
prev_command = 'S'

# Threshold value (normalized)
THRESHOLD = 0.2  # Adjust as needed. Values will be between 0 (center) and 1 (edge).

try:
    print("Listening for gamepad input...")
    for event in gamepad.read_loop():
        # Initialize command to 'Stop' at the start of each iteration
        command = 'S'
        
        # If a joystick move event occurs
        if event.type == ecodes.EV_ABS:

            normalized_value = event.value / 255.0  # Assuming joystick values range from 0 to 255

            # Joystick left and right (X-axis)
            if event.code == ecodes.ABS_X:
                if normalized_value < THRESHOLD:  # Left
                    command = 'L'
            
            # Joystick up and down (Y-axis)
            elif event.code == ecodes.ABS_Y:
                if normalized_value < THRESHOLD:  # Up/Forward
                    command = 'F'

            # If the new command differs from the previous one, send it to Arduino
            if command != prev_command:
                ser.write(command.encode())
                print(f"Sent command: {command} value: {normalized_value}")
                prev_command = command

except KeyboardInterrupt:
    # Close the serial connection
    ser.close()
    print("\nProgram terminated!")
