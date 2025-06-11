import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk
import time
import threading
from queue import Queue
import os
from datetime import datetime, timedelta

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

        # Soukya-inspired colors (background updated to solid color)
        self.colors = {
            'background': '#F6CEFC',  # Solid background color
            'text_primary': '#1a1a1a',
            'text_secondary': '#333333',
            'button_bg': '#ffe48f',
            'button_hover': '#ffd43b'
        }

        self.load_animations()
        self.start_notification_processing()

        # Load Soukya logo
        try:
            logo_image = Image.open("assets/soukya_logo.png")
            logo_image = logo_image.resize((30, 30), Image.Resampling.LANCZOS)
            self.soukya_logo = ImageTk.PhotoImage(logo_image)
        except Exception as e:
            print(f"Error loading Soukya logo: {str(e)}")
            self.soukya_logo = None

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

    def create_rounded_background(self, canvas, width, height, radius=15):
        # Create a rounded rectangle using ovals and rectangles
        # Draw the main background
        canvas.create_rectangle(0, 0, width, height, fill='white', outline='')  # Background to match system

        # Draw the rounded rectangle
        # Top-left corner
        canvas.create_oval(0, 0, radius * 2, radius * 2, fill=self.colors['background'], outline='')
        # Top-right corner
        canvas.create_oval(width - radius * 2, 0, width, radius * 2, fill=self.colors['background'], outline='')
        # Bottom-left corner
        canvas.create_oval(0, height - radius * 2, radius * 2, height, fill=self.colors['background'], outline='')
        # Bottom-right corner
        canvas.create_oval(width - radius * 2, height - radius * 2, width, height, fill=self.colors['background'], outline='')
        # Fill the sides and center
        canvas.create_rectangle(radius, 0, width - radius, height, fill=self.colors['background'], outline='')
        canvas.create_rectangle(0, radius, width, height - radius, fill=self.colors['background'], outline='')



    def open_settings(self):
        # Import SettingsWindow here to avoid circular imports
        from settings import SettingsWindow
        self.settings_window = SettingsWindow(self.root)
        self.settings_window.window.protocol("WM_DELETE_WINDOW", self.on_settings_close)
        self.settings_window.window.lift()
        self.settings_window.window.focus_force()

    def on_settings_close(self):
        if self.settings_window and self.settings_window.window.winfo_exists():
            self.settings_window.window.destroy()
        self.settings_window = None

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
                # Attempt to set transparency (works on Windows, may not on other platforms)
                self.notification_window.attributes('-transparentcolor', 'white')
            except:
                pass

            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = 300
            window_height = 130
            x = screen_width - window_width - 30
            y = screen_height - window_height - 60
            self.notification_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            canvas = tk.Canvas(self.notification_window, width=window_width, height=window_height,
                               highlightthickness=0, bd=0, bg='white')
            canvas.pack(fill='both', expand=True)

            self.create_rounded_background(canvas, window_width, window_height, radius=15)

            # Add Soukya logo at the top-left corner
            if self.soukya_logo:
                canvas.create_image(15, 10, image=self.soukya_logo, anchor='nw')

            # Add app name "Soukya" below the logo (adjusted for smaller width)
            canvas.create_text(50, 20, text="Soukya", font=('Gabriola', 20, 'bold'), anchor='w', fill=self.colors['text_primary'])

            # Add settings button (three dots) on the top-right
            settings_btn = tk.Button(self.notification_window, text="…", font=('Segoe UI', 14, 'bold'),
                                     bg=self.colors['background'], bd=0, command=self.open_settings,
                                     relief='flat')
            canvas.create_window(window_width - 60, 15, window=settings_btn, anchor='center')

            # Add close button (✕) to the left of the settings button with proper spacing
            close_btn = tk.Button(self.notification_window, text="✕", font=('Segoe UI', 11), bg=self.colors['background'],
                                  bd=0, command=self.notification_window.destroy, relief='flat')
            canvas.create_window(window_width - 20, 18, window=close_btn, anchor='center')

            # Title
            canvas.create_text(15, 47, text=title, font=('Gabriola', 17, 'bold'), anchor='w', fill=self.colors['text_primary'])

            # Message with wrapping
            message_label = tk.Label(self.notification_window, text=message, font=('Georgia', 11),
                                     fg=self.colors['text_secondary'], bg=self.colors['background'],
                                     wraplength=window_width - 30, justify='left', anchor='w')
            canvas.create_window(15, 60, window=message_label, anchor='nw')

            # Mute button
            mute_icon = "🔇" if not self.muted else "🔊"
            mute_text = "Mute" if not self.muted else "Unmute"
            mute_btn = tk.Button(self.notification_window, text=f"{mute_icon} {mute_text}", font=('Segoe UI', 9, 'bold'),
                                 bg=self.colors['button_bg'], activebackground=self.colors['button_hover'],
                                 relief='flat', bd=0, padx=10, pady=3, command=self.toggle_mute)
            canvas.create_window(window_width - 90, window_height - 30, window=mute_btn, anchor='nw')

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

# Usage:
Notifier = ModernNotifier