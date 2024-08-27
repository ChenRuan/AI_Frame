import os
import csv
from func_filesPlayer import ImageTextDisplay

def generate_play_sequence(log_file):
    with open(log_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        play_sequence = []
        for row in reader:
            if row['play'] == 'Y':
                rating_count = int(row['rating_count'])
                total_rating = float(row['total_rating'])
                average_rating = round(total_rating / rating_count, 2) if rating_count > 0 else 'No rating'
                description = (f"Prompt: {row['prompt']}\n"
                               f"Text Description: {row['text_description']}\n"
                               f"AI Source: {row['ai_source']}\n"
                               f"Rating: {average_rating}" + ("/5" if rating_count > 0 else ""))
                play_sequence.append((row['file_name'], description))
    return play_sequence

if __name__ == "__main__":
    log_file = 'image_log.csv'

    # Generate play sequence
    play_sequence = generate_play_sequence(log_file)
    for file_name, description in play_sequence:
        print(f"File: {file_name}")
        print(description)
        print("-" * 40)

    # Use ImageTextDisplay class to play images and descriptions
    media_files = [file_name for file_name, _ in play_sequence]
    texts = [description for _, description in play_sequence]

    image_text_display = ImageTextDisplay(media_files, texts, log_file)
    image_text_display.run()
