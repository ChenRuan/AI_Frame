import configparser
import pandas as pd
from datetime import datetime, time
import requests
from openai import OpenAI

def calculate_averages(file_path, start_time, end_time):
    # Read the CSV file and ensure the header is correctly interpreted
    df = pd.read_csv(file_path)
    
    # Convert the timestamp to datetime format, explicitly specifying the format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
    
    # Filter the data within the specified time range
    mask = (df['Timestamp'] >= start_time) & (df['Timestamp'] <= end_time)
    df_filtered = df[mask]
    
    # Calculate the average value for each parameter and round to two decimal places
    result = {}
    for parameter in ["windSpeed", "lux", "temp", "hum", "rain"]:
        parameter_data = df_filtered[df_filtered['Topic'].str.contains(parameter)]
        average_value = parameter_data['Message'].astype(float).mean()
        result[parameter] = round(float(average_value), 2)  # Round to two decimal places and convert to float
    
    return result

def calculate_detector_averages(file_path, start_time, end_time):
    # Read the CSV file and ensure the header is correctly interpreted
    df = pd.read_csv(file_path)
    
    # Convert the timestamp to datetime format, explicitly specifying the format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
    
    # Filter the data within the specified time range
    mask = (df['Timestamp'] >= start_time) & (df['Timestamp'] <= end_time)
    df_filtered = df[mask]
    
    # Calculate the average value for each detector and round to two decimal places
    result = {}
    for i in range(1, 6):
        detector_topic = f"detector/no{i}"
        parameter_data = df_filtered[df_filtered['Topic'].str.contains(detector_topic)]
        average_value = parameter_data['Message'].astype(float).mean()
        result[detector_topic] = round(float(average_value), 2)  # Round to two decimal places and convert to float
    
    return result

def calculate_air_quality_average(file_path, start_time, end_time):
    # Read the CSV file and ensure the header is correctly interpreted
    df = pd.read_csv(file_path)
    
    # Convert the timestamp to datetime format, explicitly specifying the format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
    
    # Filter the data within the specified time range
    mask = (df['Timestamp'] >= start_time) & (df['Timestamp'] <= end_time)
    df_filtered = df[mask]
    
    result = {}
    # Calculate the average value for air quality and round to two decimal places
    for parameter in ["airquality/value","airquality/t3mp","airquality/6um"]:
        parameter_data = df_filtered[df_filtered['Topic'].str.contains(parameter)]
        parameter_value = parameter_data['Message'].astype(float).mean()
        result = round(float(parameter_value), 2) if not pd.isna(parameter_value) else None # Round to two decimal places and convert to float
    
    return result

def get_sunrise_sunset(lat, lon, date):
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}&formatted=0"
    response = requests.get(url)
    data = response.json()
    sunrise = datetime.fromisoformat(data['results']['sunrise']).time()
    sunset = datetime.fromisoformat(data['results']['sunset']).time()
    return sunrise, sunset

def get_time_of_day(current_time, sunrise, sunset):
    current = current_time.time()
    if current < sunrise:
        return "dawn"
    elif current < time(11, 0):
        return "morning"
    elif current < time(14, 0):
        return "noon"
    elif current < time(17, 30):
        return "afternoon"
    elif current < sunset:
        return "evening"
    else:
        return "night"

def generate_prompt(averages, template, time_of_day):
    wind_speed = averages.get('windSpeed', 'unknown')
    temperature = averages.get('temp', 'unknown')
    humidity = averages.get('hum', 'unknown')
    rain = averages.get('rain', 0)
    lux = averages.get('lux', 0)
    
    weather = "raining" if rain < 3000 else "not raining"
    
    prompt = template.format(wind_speed, weather, temperature, humidity, lux, time_of_day)
    return prompt
    
def generate_text_description(prompt):
    client = OpenAI()
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative assistant, skilled in crafting detailed and evocative prompts for image generation models."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return completion.choices[0].message.content


