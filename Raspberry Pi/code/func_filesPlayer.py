import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
import csv
import os
import subprocess

class ImageTextDisplay:
    def __init__(self, media_files, texts, log_file):
        self.media_files = media_files
        self.texts = texts
        self.log_file = log_file
        self.current_index = 0
        self.text_visible = False  # Initial mode is only image
        self.rating_window = None  # Rating window handle
        self.rating_value = 5  # Default rating value
        self.paused = False  # Pause mode flag
        self.auto_play_active = True  # Auto play flag
        self.video_playing = False  # Video playing flag
        self.video_process = None  # Handle for video process
        self.intro_mode = False  # Intro mode flag

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')

        self.text_widget = tk.Text(self.root, font=("Helvetica", 20), bg="black", fg="white", padx=40, pady=40, wrap="word", highlightthickness=0, borderwidth=0)
        self.text_widget.tag_configure("spacing", spacing1=22, spacing3=25)

        self.image_label = tk.Label(self.root, bg="black")
        self.image_label.pack(fill='both', expand=True, padx=0, pady=0)

        self.display_image(self.media_files[self.current_index])

        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<Left>', lambda e: self.previous_image())
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.bind('<Return>', lambda e: self.toggle_intro())  # Bind 'Return' (Enter) key to toggle intro mode
        self.root.bind('<m>', lambda e: self.show_rating_window())
        self.root.bind('<p>', lambda e: self.toggle_pause())  # Bind 'p' key to toggle pause mode
        self.root.bind('<q>', lambda e: self.toggle_video())  # Bind 'q' key to toggle video playback

        self.root.after(100, self.ensure_fullscreen)
        self.root.after(100, self.auto_play_next)
        self.root.after(10000, self.refresh_data)  # Schedule refresh every 10 seconds

    def ensure_fullscreen(self):
        self.root.attributes('-fullscreen', True)

    def display_image(self, image_file):
        if self.paused or self.video_playing:
            self.show_black_screen()
            return

        img = Image.open(image_file)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        img_ratio = img.width / img.height
        screen_ratio = screen_width / screen_height

        if self.intro_mode:
            # Image is wider than the screen ratio, crop width
            new_height = screen_height
            crop_width = int(img.height * screen_ratio // 2)
            crop_left = (img.width - crop_width) // 2
            crop_right = crop_left + crop_width
            img = img.crop((crop_left, 0, crop_right, img.height))

            img = img.resize((screen_width//2, screen_height), Image.Resampling.LANCZOS)
            self.text_widget.pack(side='left', fill='y', padx=20, pady=20)
            self.image_label.pack(side='right', fill='both', expand=True, padx=0, pady=0)
        else:
            if img_ratio > screen_ratio:
                # 7:4 Image: Pan left to right
                new_height = screen_height
                new_width = int(screen_height * img_ratio)
                self.start_pan(new_width, new_height, screen_width)
            else:
                # 16:9 Image: Fit the screen
                new_width = screen_width
                new_height = screen_height

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.text_widget.pack_forget()
            self.image_label.pack(fill='both', expand=True, padx=0, pady=0)

        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection

        self.update_text_widget()

    def show_black_screen(self):
        self.image_label.config(image='', bg='black')
        self.text_widget.pack_forget()

    def next_image(self):
        if not self.paused and not self.video_playing:
            self.current_index = (self.current_index + 1) % len(self.media_files)
            self.display_image(self.media_files[self.current_index])

    def previous_image(self):
        if not self.paused and not self.video_playing:
            self.current_index = (self.current_index - 1) % len(self.media_files)
            self.display_image(self.media_files[self.current_index])

    def toggle_intro(self):
        if not self.paused and not self.video_playing:
            self.intro_mode = not self.intro_mode
            self.text_visible = self.intro_mode  # Show text in intro mode
            self.display_image(self.media_files[self.current_index])

    def start_pan(self, img_width, img_height, screen_width):
        if self.paused or self.video_playing:
            return

        self.image_label.place(x=0, y=0, width=img_width, height=img_height)
        self.pan_amount = img_width - screen_width
        self.pan_step = 4
        self.pan_position = 0
        self.pan_direction = 1
        self.pan()

    def pan(self):
        if self.paused or self.text_visible or self.video_playing or self.intro_mode:
            return

        if self.pan_direction == 1:
            self.image_label.place_configure(x=-self.pan_position)
            self.pan_position += self.pan_step
            if self.pan_position >= self.pan_amount:
                self.pan_position = self.pan_amount
                self.pan_direction = -1
        else:
            self.image_label.place_configure(x=-self.pan_position)
            self.pan_position -= self.pan_step
            if self.pan_position <= 0:
                self.pan_position = 0
                self.pan_direction = 1
        self.root.after(50, self.pan)  # Adjust the panning speed here

    def auto_play_next(self):
        if self.auto_play_active and not self.paused and not self.video_playing:
            self.next_image()
        self.root.after(60000, self.auto_play_next)  # Schedule next image after 30 seconds

    def run(self):
        self.root.mainloop()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.show_black_screen()
            self.auto_play_active = False
        else:
            self.display_image(self.media_files[self.current_index])
            self.auto_play_active = True

    def show_rating_window(self):
        if self.rating_window is not None:
            return

        # Reset rating to 5 stars
        self.rating_value = 5

        self.rating_window = tk.Toplevel(self.root)
        self.rating_window.title("Rating the Image")
        self.rating_window.geometry("600x330")
        self.rating_window.configure(background='black')

        window_width = 700
        window_height = 450
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.rating_window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.rating_label = tk.Label(self.rating_window, text="\nRate this image:\n", font=("Helvetica", 40), bg="black", fg="white")
        self.rating_label.pack(pady=5)

        self.rating_stars = tk.Label(self.rating_window, text="\u2605\u2605\u2605\u2605\u2605", font=("Helvetica", 55), bg="black", fg="white")
        self.rating_stars.pack()

        self.rating_instruction = tk.Label(self.rating_window, text="\nUse left/right keys to adjust rating.\n\nPress the rate button to submit.", font=("Helvetica", 25), bg="black", fg="white")
        self.rating_instruction.pack(pady=5)

        self.rating_window.bind('<Left>', lambda e: self.change_rating(-1))
        self.rating_window.bind('<Right>', lambda e: self.change_rating(1))
        self.rating_window.bind('<m>', lambda e: self.submit_rating())
        self.rating_window.protocol("WM_DELETE_WINDOW", self.close_rating_window)

    def change_rating(self, delta):
        self.rating_value = max(1, min(5, self.rating_value + delta))
        self.rating_stars.config(text="\u2605" * self.rating_value + "\u2606" * (5 - self.rating_value))

    def submit_rating(self):
        # Update the CSV file with the new rating
        self.update_rating_in_csv(self.rating_value)
        self.update_text_widget()  # Refresh the text widget with new rating
        self.close_rating_window()

    def close_rating_window(self):
        self.rating_window.destroy()
        self.rating_window = None

    def update_rating_in_csv(self, rating):
        with open(self.log_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        for row in rows:
            if row['file_name'] == self.media_files[self.current_index]:
                row['rating_count'] = int(row['rating_count']) + 1
                row['total_rating'] = round(float(row['total_rating']) + rating, 2)
                break

        with open(self.log_file, 'w', newline='') as csvfile:
            fieldnames = ['file_name', 'prompt', 'text_description', 'ai_source', 'mode', 'rating_count', 'total_rating', 'play']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def update_text_widget(self):
        with open(self.log_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        for row in rows:
            if row['file_name'] == self.media_files[self.current_index]:
                rating_count = int(row['rating_count'])
                total_rating = float(row['total_rating'])
                average_rating = round(total_rating / rating_count, 2) if rating_count > 0 else 'No rating'
                description = (f"Prompt: {row['prompt']}\n"
                               f"Text Description: {row['text_description']}\n"
                               f"AI Source: {row['ai_source']}\n"
                               f"Rating: {average_rating}" + ("/5" if rating_count > 0 else ""))
                break

        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, description, "spacing")

    def refresh_data(self):
        """Refresh media files and texts from the log file."""
        new_media_files, new_texts = self.load_data_from_log()
        if new_media_files != self.media_files:
            self.media_files = new_media_files
            self.texts = new_texts
            self.current_index = 0  # Reset to the first image
            self.display_image(self.media_files[self.current_index])
        self.root.after(30000, self.refresh_data)  # Schedule next refresh in 10 seconds

    def load_data_from_log(self):
        """Load media files and texts from the log file."""
        media_files = []
        texts = []
        with open(self.log_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['play'] == 'Y':
                    media_files.append(row['file_name'])
                    rating_count = int(row['rating_count'])
                    total_rating = float(row['total_rating'])
                    average_rating = round(total_rating / rating_count, 2) if rating_count > 0 else 'No rating'
                    description = (f"Prompt: {row['prompt']}\n"
                                   f"Text Description: {row['text_description']}\n"
                                   f"AI Source: {row['ai_source']}\n"
                                   f"Rating: {average_rating}" + ("/5" if rating_count > 0 else ""))
                    texts.append(description)
        return media_files, texts

    def toggle_video(self):
        if self.video_playing:
            self.stop_video()
        else:
            self.play_video()

    def play_video(self):
        video_path = "./src/video.mp4"  # Replace with the actual video file path
        if not os.path.exists(video_path):
            messagebox.showerror("Error", f"Video file not found: {video_path}")
            return

        self.paused = True
        self.video_playing = True
        self.show_black_screen()

        self.video_process = subprocess.Popen(
            [
                "mpv",
                "--fullscreen",
                "--no-border",
                "--loop",
                "--input-conf=/dev/null",
                "--vo=opengl",  # 使用opengl作为视频输出驱动
                "--cache=yes",        # 启用缓存
                "--cache-secs=10",    # 设置缓存时间为10秒
                video_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        self.root.after(100, self.check_video_end)

    def check_video_end(self):
        if self.video_process and self.video_process.poll() is not None:
            self.stop_video()
        elif self.video_playing:
            self.root.after(100, self.check_video_end)

    def stop_video(self):
        if self.video_process is not None:
            self.video_process.terminate()
            self.video_process.wait()
            self.video_process = None

        self.paused = False
        self.video_playing = False
        self.display_image(self.media_files[self.current_index])

# Example usage
if __name__ == "__main__":
    log_file = 'image_log.csv'
    media_files = ['test1.png', 'test2.png']
    texts = [
        "Prompt: Example prompt\nText Description: Example description\nAI Source: Example AI\nRating: No rating",
        "Prompt: Another prompt\nText Description: Another description\nAI Source: Another AI\nRating: No rating"
    ]

    image_text_display = ImageTextDisplay(media_files, texts, log_file)
    image_text_display.run()
