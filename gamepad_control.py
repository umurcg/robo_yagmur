import serial
from evdev import InputDevice, categorize, ecodes

# Setup serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Set up the gamepad device
gamepad = InputDevice('/dev/input/event2')

# Initial command to 'Stop'
prev_command = 'S'

# Threshold values
THRESHOLD_MIN = 115  # Adjust as needed
THRESHOLD_MAX = 140  # Adjust as needed

try:
    print("Listening for gamepad input...")
    for event in gamepad.read_loop():
        # If a joystick move event occurs
        if event.type == ecodes.EV_ABS:

            # Joystick left and right (X-axis)
            if event.code == ecodes.ABS_X:
                if event.value < THRESHOLD_MIN:  # Left
                    command = 'L'
                elif event.value > THRESHOLD_MAX:  # Right
                    command = 'R'
                else:
                    command = 'S'
            
            # Joystick up and down (Y-axis)
            elif event.code == ecodes.ABS_Y:
                if event.value < THRESHOLD_MIN:  # Up/Forward
                    command = 'F'
                elif event.value > THRESHOLD_MAX:  # Down/Backward
                    command = 'B'
                else:
                    command = 'S'

            # If the new command differs from the previous one, send it to Arduino
            if command != prev_command:
                ser.write(command.encode())
                print(f"Sent command: {command}")
                prev_command = command

except KeyboardInterrupt:
    # Close the serial connection
    ser.close()
    print("\nProgram terminated!")
