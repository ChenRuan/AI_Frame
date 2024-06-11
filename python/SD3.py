import requests
from img_open import crop_and_open_image
from datetime import datetime

PROMPT = ("It is 14:10 on May 8, 2024, the temperature is 8 degrees, the weather is thunder with heavy rain and force 10 wind. "
          "Please draw me the scene and surroundings of Hangzhou now, including the weather, clouds, pedestrians and so on.")
CONTROL_STRENGTH = 0.9

current_time = datetime.now().strftime("%Y%m%d%H%M%S")

response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
        "authorization": f"Bearer sk-STtCRgpstKEIEqQCFPibKEG7ys5cC3sQr1fM8VSmgj2Ey9CW",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": PROMPT,
        "control_strength": CONTROL_STRENGTH,
        "output_format": "png",
        "negative_prompt":""
    },
)

if response.status_code == 200:
    image_path_origin = f"./src/SD_{current_time}_origin.png"
    image_path_resized = f"./src/SD_{current_time}_resized.png"
    log_file_path = f"./src/log_{current_time}.txt"

    with open(image_path_origin, 'wb') as file:
        file.write(response.content)
    crop_and_open_image(image_path_origin, image_path_resized)
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Image generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"  Engine: Stable Diffusion 3\n")
        log_file.write(f"  Prompt: '{PROMPT}'\n")        
        log_file.write(f"  Control Strength: '{CONTROL_STRENGTH}'\n")
        
else:
    raise Exception(str(response.json()))
