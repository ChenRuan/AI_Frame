# Weather Station

## Project Overview
The Weather Station is designed to monitor various environmental conditions, including temperature, humidity, wind speed, and light intensity. The data collected is transmitted to an MQTT server for further processing and visualization.

## System Components

- **Arduino Nano ESP32**: Handles sensor data collection and Wi-Fi communication.
- **DHT22 Sensor**: Measures temperature and humidity.
- **BH1750 Sensor**: Measures light intensity.
- **Rain Sensor**: Detects rain.
- **Wind Speed Sensor**: Tracks wind speed.
- **Solar Power Module**: Provides power management and solar charging.

## Circuit Setup

![image](https://github.com/user-attachments/assets/71fdafd3-25e8-47e1-b802-e693fde4702c)

![image](https://github.com/user-attachments/assets/52358fb1-7ca0-4cfb-99c3-e8db1b52cad6)

![image](https://github.com/user-attachments/assets/30bb7bd9-f0dc-43f1-843e-42c9c0fafe8f)

1. Connect the DHT22 and Rain Sensor to the Arduino Nano ESP32 as per the circuit diagram.
2. Connect the BH1750 via I2C to the Arduino Nano ESP32.
3. Connect the Wind Speed Sensor to the appropriate GPIO pin on the Arduino.
4. Wire the Solar Power Module to power the Arduino.

PCB design is also provided as a garber file.

## Enclosure 

![image](https://github.com/user-attachments/assets/ca384b1a-2720-4938-85bf-3ff24d757ec1)

The enclosure for the Weather Station is designed to protect the internal components from environmental elements while allowing adequate ventilation for the sensors. All related files can be found in the enclosure folder. This includes:

1. A fully assembled Fusion 360 file (weather_station.fusion360).
2. Individual STL files for each component.

## Code

![image](https://github.com/user-attachments/assets/c8a0f0ec-58e5-45ee-a3df-727f42430448)

1. Install the required Arduino libraries: `DHT sensor library`, `Adafruit Unified Sensor`, and `BH1750`.
2. Upload the provided code to the Arduino Nano ESP32.
3. Ensure that the device connects to your Wi-Fi and begins transmitting data to the MQTT server.

## Deployment

Once powered, the Weather Station will automatically start collecting and transmitting environmental data. Put it in a sunny place and get ready to receive data!

![image](https://github.com/user-attachments/assets/1f29047e-ef34-4742-86c7-a682671c6f96)

![image](https://github.com/user-attachments/assets/027481d2-d8bd-48ba-b97b-4c00e568d0b9)
