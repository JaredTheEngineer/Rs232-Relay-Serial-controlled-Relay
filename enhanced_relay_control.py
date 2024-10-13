import serial
import time

# Configure your COM port here
com_port = 'COM11'  # Replace with your actual COM port (COM11 as per your info)

# Function to send a command to the relay and display the response
def send_relay_command(command, description):
    try:
        # Open the serial port
        ser = serial.Serial(com_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
        print(f"\nOpened port {com_port} successfully.")
        
        # Send the command
        print(f"Executing command: {description}")
        ser.write(command)
        time.sleep(0.5)  # Wait for response time
        
        # Read the response (8 bytes expected)
        response = ser.read(8)
        if response:
            print("Response:", response.hex())
        else:
            print("No response received.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    finally:
        ser.close()
        print("Serial port closed.")

# Main script
def main():
    while True:
        # Menu of options
        print("\nSelect a command to send:")
        print("1. Turn Channel ON")
        print("2. Turn Channel OFF")
        print("3. Check Channel Status")
        print("4. Toggle Channel State")
        print("5. Momentary Channel Activation (200ms)")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        # Turn channel ON/OFF
        if choice == '1' or choice == '2':
            channel = input("Enter channel number (1, 2, 3, or 4): ")
            state = "ON" if choice == '1' else "OFF"
            
            # Determine the appropriate command
            if channel == '1':
                command = bytes.fromhex("55 56 00 00 00 01 01 AD") if state == "ON" else bytes.fromhex("55 56 00 00 00 01 02 AE")
            elif channel == '2':
                command = bytes.fromhex("55 56 00 00 00 02 01 AE") if state == "ON" else bytes.fromhex("55 56 00 00 00 02 02 AF")
            elif channel == '3':
                command = bytes.fromhex("55 56 00 00 00 03 01 AF") if state == "ON" else bytes.fromhex("55 56 00 00 00 03 02 B0")
            elif channel == '4':
                command = bytes.fromhex("55 56 00 00 00 04 01 B0") if state == "ON" else bytes.fromhex("55 56 00 00 00 04 02 B1")
            else:
                print("Invalid channel number.")
                continue
            send_relay_command(command, f"Channel {channel} {state}")
        
        # Check channel status
        elif choice == '3':
            # Check Channel Status
            command = bytes.fromhex("55 56 00 00 00 00 00 AB")
            send_relay_command(command, "Check Channel Status")
        
        # Toggle Channel State
        elif choice == '4':
            channel = input("Enter channel number (1, 2, 3, or 4): ")
            
            # Toggle command for each channel
            if channel == '1':
                command = bytes.fromhex("55 56 00 00 00 01 03 AF")
            elif channel == '2':
                command = bytes.fromhex("55 56 00 00 00 02 03 B0")
            elif channel == '3':
                command = bytes.fromhex("55 56 00 00 00 03 03 B1")
            elif channel == '4':
                command = bytes.fromhex("55 56 00 00 00 04 03 B2")
            else:
                print("Invalid channel number.")
                continue
            send_relay_command(command, f"Toggle Channel {channel}")

        # Momentary Channel Activation
        elif choice == '5':
            channel = input("Enter channel number (1, 2, 3, or 4): ")

            # Momentary command for each channel
            if channel == '1':
                command = bytes.fromhex("55 56 00 00 00 01 04 B0")
            elif channel == '2':
                command = bytes.fromhex("55 56 00 00 00 02 04 B1")
            elif channel == '3':
                command = bytes.fromhex("55 56 00 00 00 03 04 B2")
            elif channel == '4':
                command = bytes.fromhex("55 56 00 00 00 04 04 B3")
            else:
                print("Invalid channel number.")
                continue
            send_relay_command(command, f"Momentary Channel {channel} Activation")

        # Exit
        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 6.")

# Run the main function
if __name__ == "__main__":
    main()
