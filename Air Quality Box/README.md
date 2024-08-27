# Air Quality Box

## Project Overview
The Air Quality Box is designed to monitor indoor air quality by measuring various environmental parameters such as temperature, humidity, and harmful gas concentrations (e.g., CO2, ammonia, and smoke). The collected data is transmitted to an MQTT server for real-time analysis and visualization.

## System Components
- **ESP8266**: Handles sensor data collection and Wi-Fi communication.
- **DHT22 Sensor**: Measures temperature and humidity.
- **MQ-135 Gas Sensor**: Detects harmful gases like CO2, ammonia, benzene, and smoke.
- **Custom PCB**: Optimizes circuit layout and connections for the components.
- **USB Power Supply**: Provides stable power to the system.

## Circuit Setup
1. Connect the DHT22 sensor to the ESP8266 following the circuit diagram.
2. Attach the MQ-135 sensor to the designated GPIO pins on the ESP12E.
3. Use the USB power supply to power the ESP8266 via the VIN pin.
4. Assemble all components on the custom PCB to ensure a compact and organized setup.
![image](https://github.com/user-attachments/assets/0612b455-08f3-4f98-9d80-d19d76ae141a)
![image](https://github.com/user-attachments/assets/224a74b4-a420-4c11-af56-2812af602dc2)

## Code Deployment
1. Install the required libraries for the ESP8266, including `DHT sensor library` and `MQTT`.
2. Upload the provided code to the ESP8266 microcontroller. Don't forget to replace username, password, mqtt server, etc.
3. Ensure the device connects to Wi-Fi and starts sending data to the MQTT server.

## Usage
Once powered, the Air Quality Box will automatically begin monitoring the indoor environment, sending real-time data on air quality to the MQTT server for further analysis.

