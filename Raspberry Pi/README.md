# Raspberry Pi 

## Project Overview
This project involves using a Raspberry Pi to process environmental data collected from various sensor systems (Weather Station, Detection Box, and Air Quality Box) and to manage user interaction devices that display AI-generated visualizations based on the collected data. The system processes the sensor data, sends it to an MQTT server, generates AI-based visual images, and displays the information through an interactive device.

![image](https://github.com/user-attachments/assets/a15d6d24-006c-4e73-8ffb-d7035f6c6a8e)

![image](https://github.com/user-attachments/assets/a0b27302-deef-4bdf-add2-76a492f29277)

![image](https://github.com/user-attachments/assets/05a9058c-c630-4384-9640-800c83c88d5b)

## System Components
- **Raspberry Pi 4 Model B**: Central processing unit for handling data collection, processing, and user interaction.
- **Capacitive Buttons with LEDs**: Interface for user interaction, allowing navigation through the displayed images.
- **MPU6050 Module (optional)**: Provides gravity detection, although not used in the final implementation.
- **DALL-E API / Stable Diffusion API**: Used for generating AI-based images from sensor data.
- **HDMI Display**: Used for the interactive display.

## Enclosure Design
The Raspberry Pi and related components are housed in a custom enclosure designed to provide protection while ensuring adequate ventilation. The design files for the enclosure are available in the `enclosure` folder, which includes:
- PDF files for UV printing.
- Individual STL files for each part.

![image](https://github.com/user-attachments/assets/145f7e68-151a-46bd-8c8d-40be096a497a)

## Setup Instructions

### 1. Hardware Assembly

![image](https://github.com/user-attachments/assets/ceb9f380-cd8b-4be0-8a1a-59ff719a8730)

1. **Connect the Capacitive Buttons**: 
   - Wire the capacitive buttons to the designated GPIO pins on the Raspberry Pi.
   - Ensure LEDs are correctly connected to indicate button activation.

2. **Optional MPU6050 Module**:
   - Connect the MPU6050 to the Raspberry Pi using the I2C interface. 
   - This module is optional and not required for the primary functionality.

3. **Connect the Raspberry Pi to Power**:
   - Ensure the Raspberry Pi is properly powered using a 5V/3A power supply.

### 2. Software Installation

1. **Update the Raspberry Pi OS**:
   ```
   sudo apt-get update
   sudo apt-get upgrade
   ```

2. **Install Required Libraries**:
   ```
   sudo apt-get install python3 python3-pip
   pip3 install requests pandas openai pillow configparser
   sudo apt-get install python3-gpiozero
   sudo apt-get install python3-rpi.gpio python3-spidev python3-pip python3-pil python3-numpy python3-smbus
   sudo apt-get install python3-pil python3-pil.imagetk
   ...
   ```
   
   Please download other libraries as needed.
   
### 3. Data Processing

![image](https://github.com/user-attachments/assets/41bafbcf-a15a-4e0e-9d1b-d1a8801308ce)

#### 1. Setup Configuration File

Make sure you have the correct prompt template in `config.ini`.

#### 2. Deploy the Data Processing Scripts

Place the provided Python scripts in a designated directory on the Raspberry Pi:

##### 1. mqtt.py

**Purpose**: This script is used to collect data from MQTT and store the collected data in `mqtt_data.csv`.

##### 2. gpiotest.py

**Purpose**: This script is used to map key triggers on the box to keyboard inputs.

##### 3. generate.py

**Purpose**: This script first reads the data in the stored mqtt_data.csv and generates the first prompt using the configuration in config.ini. after importing this prompt into ChatGPT 4o mini, it lets it generate a second prompt for generating images. this prompt is imported into the corresponding image generating AI model ( DALL-E-3 or StableDiffusion), generate the picture, download it locally and log it. The script calls the following three functions.

##### 4. func_data.py

**Purpose**: This function is used to read and process data from mqtt_data.csv, to convert data that is difficult for the AI to recognise (e.g. air quality, rainfall parameters), etc., into understandable data, and to provide an interface function for transferring the ChatGPT 4o mini.

##### 5. func_sd.py

**Purpose**: This function is used to call StableDiffusion and generate images to be downloaded locally.

##### 6. func_dalle3.py

**Purpose**: This function is used to call DALL-E-3 and generate images to be downloaded locally.

##### 7. image.py

**Purpose**: This script is used to process the data in `image_log.csv` and call the `func_filesPlayer` function to display the image.

##### 8. func_filesPlayer.py

**Purpose**: This function is used to implement the interface to interact with the user, including autoplay, button control, mode switching, video playback and other functions.

![image](https://github.com/user-attachments/assets/eb3e6f89-a6a4-4389-a4a7-170e8f47b242)

#### 3. Running the Data Processing

The following functions are launched residently for data collection and key mapping (you can use the pm2 utility for power-on self-start):

```
python mqtt.py
python gpiotest.py
```

The following function can be called at regular intervals to generate a new image based on the environment data

```
python generate.py
```

Use the following command to open the user interaction interface
```
python image.py
```

### 4. Interactive Display Setup

#### 1. Hardware Setup

- Connect the HDMI display to the Raspberry Pi.
- Adjust the resolution of the display to 1920*1080 (you can also modify the parameters inside func_filesPlayer.py to fit the screen)
 
#### 2. User Interaction
- Next Image: Press the right button.
- Previous Image: Press the left button.
- Rate Image: Press the rating button and use left/right keys to adjust the rating.
- Pause/Resume Slideshow: Press the pause button.
- Play Video: Press the video button (make sure the video file is in the correct path).

### 5. Web Dashboard

![image](https://github.com/user-attachments/assets/a1925a30-4db9-4017-aa9e-ad0ed64e7f3e)

![image](https://github.com/user-attachments/assets/d854696b-0d53-4615-bae4-0ef189f1274b)

#### 1. Node-RED Setup

- Start Node-RED:
```
node-red-start
```
- Access the dashboard via `http://<your-raspberry-pi-ip>:1880`.
- Importing `flow.js` to complete the configuration of the page (It contains three dashboards, image download page and feedback page, please adjust as needed)

#### 2. ngrok Setup (Optional)
- Register and setup on ngrok (please follow the official instructions)
- Expose the dashboard to the internet using ngrok:
```
sudo snap install ngrok
ngrok http 1880
```
