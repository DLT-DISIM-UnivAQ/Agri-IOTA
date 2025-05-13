import subprocess
import time
import random
import serial
 
# Define the IOTA client call to log sensor data
def log_sensor_data(sensor_id, humidity, temperature, soil_temperature, timestamp):
    # Construct the command for the IOTA client call
    command = [
        'iota', 'client', 'call',
        '--package', '0xb8f5a36f9ff7adee8c14a638cbff1773748917c60b2159ded8d456beacb29acc',  # Replace with your package ID
        '--module', 'AgricultureMonitoring',  # Your module name
        '--function', 'log_sensor_data',  # Function you defined in Move module
        '--args', str(sensor_id), str(humidity), str(temperature), str(soil_temperature), str(timestamp),
        '--gas-budget', '100000000'  # Adjust gas budget as needed
    ]
   
    try:
        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("Sensor data logged successfully!")
            return result.stdout
        else:
            print(f"Error logging data: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error running IOTA client: {e}")
        return None
 
# Configure the serial port for receiving data from the Raspberry Pi Pico
port = '/dev/ttyACM0'  # Replace with the correct port where the Pico is connected
baudrate = 9600
 
# Process data from the Raspberry Pi Pico and send it to IOTA
try:
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"Connected to port {port}. Receiving data...")
        while True:
            # Read data sent by the Pico
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Data received: {line}")
               
                # Split the data based on the delimiter ";"
                parts = line.split(";")
                if len(parts) == 4:
                    try:
                        sensor_id = int(parts[0].split(":")[1].strip())
                        ambient_temperature = float(parts[1].split(":")[1].strip().replace("C", ""))
                        soil_humidity = float(parts[2].split(":")[1].strip().replace("%", ""))
                        soil_temperature = float(parts[3].split(":")[1].strip().replace("C", ""))
                       
                        # Ensure data types match the Move function's requirements
                        humidity = int(min(max(soil_humidity, 0), 255))  # Clamp to range 0-255
                        temperature = int(min(max(ambient_temperature, 0), 255))
                        soil_temperature = int(min(max(soil_temperature, 0), 255))
                       
                        # Generate additional data
                        timestamp = int(time.time())
                       
                        # Log data to IOTA
                        log_sensor_data(sensor_id, humidity, temperature, soil_temperature, timestamp)
                    except Exception as e:
                        print(f"Error processing the received data: {e}")
            time.sleep(0.1)
except serial.SerialException as e:
    print(f"Connection error: {e}")