import os
import requests
from datetime import datetime
from openai import OpenAI

def generate_and_download_image(prompt, output_directory, image_name):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Initialize the OpenAI client
    client = OpenAI()
    
    # Get the current timestamp for logging
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = os.path.join(output_directory, image_name)
    log_file_path = os.path.join(output_directory, f"{image_name}_log_{current_time}.txt")
    
    # Generate the image using OpenAI's API
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    
    # Get the image URL from the response
    image_url = response.data[0].url
    print(image_url)
    
    # Download the image
    img_response = requests.get(image_url)
    with open(image_path, 'wb') as image_file:
        image_file.write(img_response.content)
    
    return f"{image_path}"
