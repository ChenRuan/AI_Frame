# Visualising the Environment: How AI-Generated Art Transforms Data into Understanding

## Project Background and Purpose

The Environmental Data Visualization System is an innovative project aimed at making complex environmental data accessible through visually intuitive AI-generated art. By leveraging custom-built sensor systems, the project captures real-time environmental data and transforms it into artistic visualizations, bridging the gap between technical information and broader public understanding.

![c35c359a0689a05a3d456027376dfbe](https://github.com/user-attachments/assets/63200c26-b868-4f88-ab18-d052bdd291d2)

## System Architecture

The system is composed of several interconnected components:

1. **Data Collection**: Utilizes three main sensor systems—Weather Station, Detection Box, and Air Quality Box—to gather data from different environments.
2. **Data Processing**: Handled by the Raspberry Pi, which converts the collected data into natural language prompts for AI models.
3. **AI Image Generation**: AI models such as DALL-E 3 and Stable Diffusion generate images based on the processed data.
4. **User Interaction**: A web dashboard provides real-time data monitoring and an interface for viewing generated images.

![1724425097138](https://github.com/user-attachments/assets/02354a3a-40ca-4162-9e14-5d46537ed9af)

## Sensor Systems Overview

### Weather Station

Monitors weather conditions including temperature, humidity, wind speed, and rain. Data is sent to the MQTT server and then processed for visualization.

### Portable Detection Box

Tracks visitor movement in exhibition spaces, providing valuable data for generating visual representations of crowd patterns.

### Air Quality Box

Measures indoor air quality by detecting harmful gases and environmental conditions, feeding data into the AI system for analysis and visualization.

## Getting Started

To begin using the system, please refer to the detailed setup instructions provided for each component:

- [Weather Station Setup](Weather%20Station/README.md)
- [Detection Box Setup](Portable%20Detection%20Box/README.md)
- [Air Quality Box Setup](Air%20Quality%20Box/README.md)
- [Raspberry Pi Setup](Raspberry%20Pi/README.md)

## License

This project is licensed under the MIT License.
