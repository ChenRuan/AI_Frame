import subprocess
from PIL import Image

def crop_and_open_image(image_path_origin, image_path_resized):
        def crop_to_aspect_ratio(input_path, output_path, size=(1920, 1080)):
            with Image.open(input_path) as img:
                width, height = img.size
                target_width, target_height = size

                scale = max(target_width / width, target_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                left = (new_width - target_width) / 2
                top = (new_height - target_height) / 2 + 150
                right = (new_width + target_width) / 2
                bottom = (new_height + target_height) / 2 + 150
                
                top = max(0, min(top, new_height - target_height))
                bottom = max(target_height, min(bottom, new_height))

                img_cropped = img.crop((left, top, right, bottom))
                img_cropped.save(output_path)
                
        crop_to_aspect_ratio(image_path_origin, image_path_resized)
                
        subprocess.Popen(['feh', '--fullscreen', '--hide-pointer', '--no-menus', image_path_resized])
