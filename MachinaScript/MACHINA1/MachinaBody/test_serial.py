import serial
import time

# Replace 'COM3' with the correct port for your Arduino
arduino_port = "COM3"  #  change the port of your arduino
# arduino_port = "/dev/ttyACM0"  # for Linux/Mac
baud_rate = 9600

# Initialize serial connection to the Arduino
arduino_serial = serial.Serial(arduino_port, baud_rate, timeout=1)

def send_command(command):
    # Append the newline character to the command
    full_command = command + "\n"
    print(f"Sending command: {full_command}")
    arduino_serial.write(full_command.encode())
    time.sleep(2)  # Wait for the Arduino to process the command

def main():
    try:
        # List of commands to send
        commands = [
            "A:45,10;B:0,10;",
            "A:0,10;B:45,10;",
            "A:90,10;B:180,20;"
        ]

        for command in commands:
            send_command(command)

        print("Commands sent.")
    finally:
        # Close the serial connection
        arduino_serial.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()
