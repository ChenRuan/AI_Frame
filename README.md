# Visualising the Environment: How AI-Generated Art Transforms Data into Understanding

This project is designed to transform complex environmental data into visually intuitive images using AI-generated art. By integrating various sensor systems with advanced AI models, this project offers a unique approach to understanding and engaging with environmental data.
![c35c359a0689a05a3d456027376dfbe](https://github.com/user-attachments/assets/63200c26-b868-4f88-ab18-d052bdd291d2)

## Project Overview

![1724425097138](https://github.com/user-attachments/assets/02354a3a-40ca-4162-9e14-5d46537ed9af)

The system is designed with modularity and scalability in mind, making it adaptable for various environmental monitoring needs. The core architecture involves:

- **Data Collection**: Collect data from the sensor system.
- **Data Processing**: Managed by the Raspberry Pi, which prepares the data for AI image generation.
- **User Interaction**: A user-friendly interface allows users to interact with the system, view generated images, and monitor data in real-time through a web dashboard.

The sensor system consists of three main components:

1. **Weather Station**: Captures weather data like temperature, humidity, and wind speed, and sends it to an MQTT server.
2. **Detection Box**: Monitors visitor movement in exhibition spaces, providing real-time data for visualization.
3. **Air Quality Box**: Measures indoor air quality by detecting harmful gases and environmental parameters.

Each component sends its data to the Raspberry Pi, where it is processed and converted into natural language prompts. These prompts are then used by AI models like DALL-E 3 or Stable Diffusion to generate artistic visual representations of the data.

## Deployment

Deploying the system involves setting up the sensor devices in their respective environments, connecting them to the MQTT server, and running the Raspberry Pi scripts to handle data processing and user interaction. The web dashboard allows for remote access and monitoring.

## Getting Started

To get started, follow the instructions in each component's README file:

- [Weather Station Setup](Weather_Station/README.md)
- [Detection Box Setup](Portable_Detection_Box/README.md)
- [Air Quality Box Setup](Air_Quality_Box/README.md)
- [Raspberry Pi Setup](Raspberry_pi/README.md)
