import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk
import time
import threading
from queue import Queue
import os
from datetime import datetime, timedelta
import traceback

class ModernNotifier:
    def __init__(self, settings):
        print("Modern Notifier initialized")
        self.settings = settings
        self.muted = settings.get('muted', False)
        self.notification_queue = Queue()
        self.current_notification = None
        self.animation_frames = {}
        self.animation_index = 0
        self.root = tk.Tk()
        self.root.withdraw()
        self.notification_window = None
        self.animation_label = None
        self.animation_running = False
        self.notification_frequency = settings.get('notification_frequency_minutes', 60) * 60
        self.last_notification_time = {}

        self.colors = {
            'background_top': '#b2e9f9',
            'background_bottom': '#ffd6f2',
            'text_primary': '#1a1a1a',
            'text_secondary': '#333333',
            'button_bg': '#ffe48f',
            'button_hover': '#ffd43b'
        }

        self.load_animations()
        self.start_notification_processing()

    def reload_settings(self):
        try:
            with open('config.json', 'r') as f:
                self.settings = json.load(f)
            self.muted = self.settings.get('muted', False)
            self.notification_frequency = self.settings.get('notification_frequency_minutes', 60) * 60
            print("Settings reloaded successfully")
        except Exception as e:
            print(f"Error reloading settings: {str(e)}")

    def start_notification_processing(self):
        def process_queue():
            try:
                if not self.notification_queue.empty():
                    self.process_notification()
                self.root.after(100, process_queue)
            except Exception as e:
                print(f"Error in notification processing: {str(e)}")
                self.root.after(100, process_queue)

        process_queue()

    def load_animations(self):
        animation_paths = self.settings.get('animation', {})
        for notification_type, path in animation_paths.items():
            if os.path.exists(path):
                try:
                    gif = Image.open(path)
                    frames = []
                    for frame in range(gif.n_frames):
                        gif.seek(frame)
                        frame_image = gif.copy()
                        frame_image.thumbnail((60, 60), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(frame_image)
                        frames.append(photo)
                    self.animation_frames[notification_type] = frames
                except Exception as e:
                    self.animation_frames[notification_type] = []
            else:
                self.animation_frames[notification_type] = []

    def show_notification(self, title, message, notification_type="greeting"):
        if self.muted:
            return
        self.notification_queue.put((title, message, notification_type))

    def toggle_mute(self):
        self.muted = not self.muted
        self.settings['muted'] = self.muted
        with open('config.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
        if self.muted and self.notification_window:
            self.notification_window.destroy()

    def create_gradient_background(self, canvas, width, height, color1, color2):
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        r1, g1, b1 = hex_to_rgb(color1)
        r2, g2, b2 = hex_to_rgb(color2)

        for i in range(height):
            ratio = i / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, width=1)

    def process_notification(self):
        if not self.notification_queue.empty():
            title, message, notification_type = self.notification_queue.get()

            if self.notification_window:
                self.notification_window.destroy()

            self.notification_window = tk.Toplevel(self.root)
            self.notification_window.overrideredirect(True)
            self.notification_window.attributes('-topmost', True)
            try:
                self.notification_window.attributes('-alpha', 0.98)
            except:
                pass

            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = 400
            window_height = 150
            x = screen_width - window_width - 30
            y = screen_height - window_height - 60
            self.notification_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            canvas = tk.Canvas(self.notification_window, width=window_width, height=window_height,
                               highlightthickness=0, bd=0)
            canvas.pack(fill='both', expand=True)

            self.create_gradient_background(canvas, window_width, window_height,
                                            self.colors['background_top'], self.colors['background_bottom'])

            # Notification text and buttons directly on canvas
            icon = '☀️'
            canvas.create_text(30, 35, text=icon, font=('Segoe UI', 18), anchor='w', fill=self.colors['text_primary'])
            canvas.create_text(60, 35, text=title, font=('Segoe UI', 14, 'bold'), anchor='w', fill=self.colors['text_primary'])
            canvas.create_text(30, 70, text=message, font=('Segoe UI', 11), anchor='w', fill=self.colors['text_secondary'])

            # Buttons
            close_btn = tk.Button(self.notification_window, text="✕", font=('Segoe UI', 11), bg=self.colors['background_bottom'],
                                  bd=0, command=self.notification_window.destroy, relief='flat')
            mute_icon = "🔇" if not self.muted else "🔊"
            mute_text = "Mute" if not self.muted else "Unmute"
            mute_btn = tk.Button(self.notification_window, text=f"{mute_icon} {mute_text}", font=('Segoe UI', 10, 'bold'),
                                 bg=self.colors['button_bg'], activebackground=self.colors['button_hover'],
                                 relief='flat', bd=0, padx=12, pady=4, command=self.toggle_mute)

            canvas.create_window(window_width - 100, window_height - 40, window=mute_btn, anchor='nw')
            canvas.create_window(window_width - 140, window_height - 40, window=close_btn, anchor='nw')

            self.notification_window.after(8000, self.notification_window.destroy)

    def run(self):
        def schedule_custom_reminders():
            while True:
                try:
                    current_time = datetime.now()
                    current_day = current_time.strftime("%a")
                    current_time_str = current_time.strftime("%I:%M %p")

                    self.reload_settings()

                    custom_reminders = self.settings.get("custom_reminders", [])
                    for reminder in custom_reminders:
                        reminder_key = f"{reminder['title']}{reminder['days']}{reminder['time']}"
                        last_time = self.last_notification_time.get(reminder_key)

                        if (current_day in reminder["days"] and
                            current_time_str == reminder["time"] and
                            (last_time is None or
                             (current_time - last_time) > timedelta(minutes=1))):

                            custom_message = self.settings.get("custom_message", "")
                            message = "Time for your scheduled reminder!"
                            if custom_message:
                                message += f"\n{custom_message}"
                            self.show_notification(
                                reminder["title"],
                                message,
                                "greeting"
                            )
                            self.last_notification_time[reminder_key] = current_time

                    time.sleep(60 - current_time.second)
                except Exception as e:
                    time.sleep(60)

        threading.Thread(target=schedule_custom_reminders, daemon=True).start()
        self.root.mainloop()

Notifier = ModernNotifier
