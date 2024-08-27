# Portable Detection Box

## Project Overview
The Portable Detection Box is designed to monitor human movement within specific areas, such as exhibition spaces. It tracks the flow of visitors using PIR sensors and sends the collected data to an MQTT server for analysis and further processing.
![image](https://github.com/user-attachments/assets/9c27de31-ebd9-434b-a057-a8d88b5486e7)

## System Components
- **ESP8266**: The main microcontroller unit that handles sensor data and Wi-Fi communication.
- **PIR Motion Sensor (HC-SR501)**: Detects human motion within a certain range and sends signals to the ESP8266.
- **LED Indicators**: Visual indicators for device status (operation and motion detection).
- **3-Slot AA Battery Holder**: Provides power to the system, making it portable.
- **Custom PCB**: Ensures a compact and efficient circuit layout.

## Enclosure Design
The Portable Detection Box has a custom-designed enclosure that houses all components securely. The design prioritizes portability, ease of assembly, and battery replacement. All related files can be found in the `enclosure` folder.

![image](https://github.com/user-attachments/assets/e5e2a24f-4245-41b4-8281-7cd11d35a020)

## Circuit Setup
1. Connect the PIR sensor to the ESP8266 as specified in the circuit diagram.
2. Attach the LED indicators to the designated GPIO pins on the ESP8266.
3. Connect the battery holder to the ESP8266 to supply power.
4. Ensure that the custom PCB is used to minimize space and optimize connections.
   
![image](https://github.com/user-attachments/assets/e7dea442-e292-4dd7-a24e-7bb1eb60af4e)
![image](https://github.com/user-attachments/assets/5934f392-a245-4713-bacb-41a6ad70d76c)

## Code Deployment

1. Install the necessary libraries for the ESP8266, including Wi-Fi and MQTT libraries.
2. Upload the provided code to the ESP12E microcontroller. Don't forget to replace username, password, mqtt server, etc.
3. Refer to the diagram below for the code flow
![image](https://github.com/user-attachments/assets/d3ce5936-c41b-4967-a195-8926441be1e9)

4. Ensure the device connects to Wi-Fi and starts sending data to the MQTT server.

## Usage
Once the box is powered, it will monitor the designated area for motion, triggering the PIR sensor. The collected data is then sent to the MQTT server for real-time analysis.
