from openai import OpenAI 
import requests
from datetime import datetime
from img_open import crop_and_open_image

client = OpenAI()

PROMPT = "Please draw me the scene and surroundings of Hangzhou now, including the weather, clouds, pedestrians and so on. It is 14:10 on May 8, 2024, the temperature is 8 degrees, the weather is thunder with heavy rain and force 10 wind. It should convey the atmosphere and mood suggested by the weather, with appropriate lighting and color tones. No numerical data or text should be included, just a pure visual representation of the weather in the landscape."

current_time = datetime.now().strftime("%Y%m%d%H%M%S")
image_path_origin = f"./src/DALLE_{current_time}_origin.png"
image_path_resized = f"./src/DALLE_{current_time}_resized.png"
log_file_path = f"./src/DALLE_log_{current_time}.txt"

response = client.images.generate(
  model="dall-e-3",
  prompt=PROMPT,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)
img_response = requests.get(image_url)

with open(image_path_origin, 'wb') as image_file:
    image_file.write(img_response.content)

crop_and_open_image(image_path_origin, image_path_resized)

with open(log_file_path, 'w') as log_file:
    log_file.write(f"Image generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write(f"Engine: DALL-E-3\n")
    log_file.write(f"Prompt: '{PROMPT}'\n")
    log_file.write(f"Image URL: {image_url}\n")
