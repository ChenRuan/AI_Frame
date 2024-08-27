import os
import configparser
import pandas as pd
from datetime import datetime, timedelta
import requests
from openai import OpenAI
from func_sd import generate_and_download_stablediffusion_image
from func_dalle3 import generate_and_download_image
from func_data import (
    calculate_averages,
    calculate_detector_averages,
    calculate_air_quality_average,
    get_sunrise_sunset,
    get_time_of_day,
    generate_prompt,
    generate_text_description
)
import csv

def generate_image_and_save(file_path, latitude, longitude, output_directory, config_file, ai_source, mode, prompt_type):
    # Calculate the time range for the last hour
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    # Calculate averages
    if prompt_type == 1:
        averages = calculate_averages(file_path, start_time, end_time)
    elif prompt_type == 2:
        averages = calculate_detector_averages(file_path, start_time, end_time)
    elif prompt_type == 3:
        averages = {'airquality': calculate_air_quality_average(file_path, start_time, end_time)}
    else:
        raise ValueError("Invalid prompt type specified")
    
    # Read the config file
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Select the prompt template based on the prompt type
    current_time = datetime.now()
    time_of_day = get_time_of_day(current_time, *get_sunrise_sunset(latitude, longitude, current_time.date()))
    
    if prompt_type == 1:
        template = config.get('Prompts', 'weather_prompt')
        prompt = template.format(ai_source, 
                                 averages['windSpeed'], 
                                 "raining" if averages['rain'] < 3000 else "not raining", 
                                 averages['temp'], 
                                 averages['hum'], 
                                 averages['lux'], 
                                 time_of_day)
    elif prompt_type == 2:
        template = config.get('Prompts', 'detector_prompt')
        current_time_str = current_time.strftime('%H:%M')
        template = template.format(ai_source, current_time_str)
        prompt = process_detector_template(template, averages)
    elif prompt_type == 3:
        averages = calculate_air_quality_average(file_path, start_time, end_time)
        template = config.get('Prompts', 'air_quality_prompt').format(ai_source)
        prompt = process_air_quality_template(template, averages)
    else:
        raise ValueError("Invalid prompt type specified")
    
    # Generate the text description using GPT-4o-mini
    text_description = generate_text_description(prompt)
    text_description += " Please do not include any actual number text in this image."
    
    # Generate the image using the specified AI source and save it
    current_time_str = current_time.strftime('%Y%m%d_%H%M')
    if ai_source == 'DALL-E-3':
        image_name = f"DALL_E_{current_time_str}_type{prompt_type}.png"
        image_path = generate_and_download_image(prompt, output_directory, image_name)
    elif ai_source == 'Stable Diffusion':
        image_name = f"Stable_Diffusion_{current_time_str}_type{prompt_type}.webp"
        image_path = generate_and_download_stablediffusion_image("YOUR_STABLE_DIFFUSION_API_KEY", prompt, output_directory, image_name)
    else:
        raise ValueError("Invalid AI source specified")

    return image_path, prompt, text_description, ai_source, mode

def process_detector_template(template, averages):
    # Define the text templates for each detector
    detector_text_templates = {
        1: "The percentage of time with foot traffic at the entrances is {}%.",
        2: "The percentage of time with foot traffic in the middle is {}%.",
        3: "The percentage of time with foot traffic on the left is {}%.",
        4: "The percentage of time with foot traffic at the back is {}%.",
        5: "The percentage of time with foot traffic on the right is {}%."
    }
    
    # Create a list to hold the generated texts
    detector_texts = []
    
    # Process each detector
    for i in range(1, 6):
        detector_key = f"detector/no{i}"
        if detector_key in averages and not pd.isna(averages[detector_key]):
            # Use the corresponding template and fill in the percentage
            detector_texts.append(detector_text_templates[i].format(averages[detector_key]))
    
    # Join all the detector texts into one string
    if detector_texts:
        final_text = " ".join(detector_texts)
        template = template.replace("(?)", final_text)
    else:
        template = template.replace("(?)", "")
    
    return template


def process_air_quality_template(template, averages):
    if averages is None:
        template = template.replace("(?)", "The air quality is good.")
    else:    
        air_quality_value = averages.get("airquality/value", None)
        air_temp_value = averages.get("airquality/t3mp", None)
        air_hum_value = averages.get("airquality/6um", None)
        
        # Handle air quality description
        if pd.isna(air_quality_value):
            air_quality_text = ""
        elif air_quality_value < 10:
            air_quality_text = "The air quality is poor. "
        elif 10 <= air_quality_value <= 20:
            air_quality_text = "The air quality is average. "
        else:
            air_quality_text = "The air quality is good. "
        
        # Handle additional air quality data
        if not pd.isna(air_temp_value):
            air_quality_text += f"The temperature is {air_temp_value}°C. "
        
        if not pd.isna(air_hum_value):
            air_quality_text += f"The particulate matter is {air_hum_value}μm. "
        
        # Update the template
        template = template.replace("(?)", air_quality_text.strip())
    
    return template


def update_log_file(log_file, image_name, prompt, text_description, ai_source, mode):
    fieldnames = ['file_name', 'prompt', 'text_description', 'ai_source', 'mode', 'rating_count', 'total_rating', 'play']
    log_exists = os.path.isfile(log_file)
    
    # Read the existing records if log file exists
    rows = []
    if log_exists:
        with open(log_file, 'r', newline='') as readfile:
            reader = csv.DictReader(readfile)
            rows = list(reader)
    
    with open(log_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Update existing records to set 'play' to 'N' for the same mode
        for row in rows:
            if 'mode' in row and row['mode'] == mode:
                row['play'] = 'N'
            filtered_row = {key: row[key] for key in fieldnames}
            writer.writerow(filtered_row)
        
        # Add new record
        writer.writerow({
            'file_name': image_name,
            'prompt': prompt,
            'text_description': text_description,
            'ai_source': ai_source,
            'mode': mode,
            'rating_count': 0,
            'total_rating': 0,
            'play': 'Y'
        })

def generate_weather_image(ai_source):
    file_path = 'mqtt_data.csv'
    latitude = 51.5074
    longitude = -0.1278
    output_directory = './images'
    config_file = 'config.ini'
    log_file = 'image_log.csv'
    mode = 'weather'
    prompt_type = 1  # 1 for weather

    # Generate image and save
    image_path, prompt, text_description, ai_source, mode = generate_image_and_save(file_path, latitude, longitude, output_directory, config_file, ai_source, mode, prompt_type)

    # Update log file
    update_log_file(log_file, image_path, prompt, text_description, ai_source, mode)

def generate_detector_image(ai_source):
    file_path = 'mqtt_data.csv'
    latitude = 51.5074
    longitude = -0.1278
    output_directory = './images'
    config_file = 'config.ini'
    log_file = 'image_log.csv'
    mode = 'detector'
    prompt_type = 2  # 2 for detector

    # Generate image and save
    image_path, prompt, text_description, ai_source, mode = generate_image_and_save(file_path, latitude, longitude, output_directory, config_file, ai_source, mode, prompt_type)

    # Update log file
    update_log_file(log_file, image_path, prompt, text_description, ai_source, mode)

def generate_air_quality_image(ai_source):
    file_path = 'mqtt_data.csv'
    latitude = 51.5074
    longitude = -0.1278
    output_directory = './images'
    config_file = 'config.ini'
    log_file = 'image_log.csv'
    mode = 'air_quality'
    prompt_type = 3  # 3 for air quality

    # Generate image and save
    image_path, prompt, text_description, ai_source, mode = generate_image_and_save(file_path, latitude, longitude, output_directory, config_file, ai_source, mode, prompt_type)

    # Update log file
    update_log_file(log_file, image_path, prompt, text_description, ai_source, mode)

if __name__ == "__main__":
    # Can be 'DALL-E-3' or 'Stable Diffusion'
    # Call the desired function based on the requirement
    generate_weather_image('DALL-E-3')
    generate_detector_image('Stable Diffusion')
    generate_air_quality_image('DALL-E-3')
