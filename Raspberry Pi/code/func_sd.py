import os
import requests

def generate_and_download_stablediffusion_image(api_key, prompt, output_directory, image_name):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Define the API endpoint and headers
    url = "https://api.stability.ai/v2beta/stable-image/control/sketch"
    headers = {
        "authorization": f"Bearer sk-YOURAPIKEY",
        "accept": "image/*"
    }
    # Define the data payload
    data = {
        "prompt": prompt,
        "output_format": "webp",
        "aspect_ratio": "16:9"
    }
    
    # Send the POST request to the Stable Diffusion API
    response = requests.post(url, headers=headers, files={"image": open("./src/image.jpeg", "rb")}, data=data)
    
    if response.status_code == 200:
        # Save the generated image to the specified path
        image_path = os.path.join(output_directory, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
        return f"{image_path}"
    else:
        # Raise an exception if the request was unsuccessful
        raise Exception(str(response.json()))
