import serial
from evdev import InputDevice, categorize, ecodes

# Setup serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Set up the gamepad device
gamepad = InputDevice('/dev/input/eventX')  # Replace X with the correct number for the DualSense.

# A mapping of gamepad keys to commands for the robot
key_map = {
    ecodes.KEY_UP: 'F',
    ecodes.KEY_DOWN: 'B',
    ecodes.KEY_LEFT: 'L',
    ecodes.KEY_RIGHT: 'R'
}

try:
    print("Listening for gamepad input...")
    for event in gamepad.read_loop():
        # If a key is pressed or released
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)

            # If the key is pressed and it's in our key map
            if key_event.keystate == key_event.key_down and key_event.scancode in key_map:
                command = key_map[key_event.scancode]
                ser.write(command.encode())
                print(f"Sent command: {command}")

            # If no arrow key is pressed, we assume the robot should stop.
            elif key_event.keystate == key_event.key_up:
                ser.write('S'.encode())
                print("Sent command: Stop")

except KeyboardInterrupt:
    # Close the serial connection
    ser.close()
    print("\nProgram terminated!")
