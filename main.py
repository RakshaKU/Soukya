import json
import os
import threading
import time
from datetime import datetime
from notifier import Notifier
from settings import SettingsWindow
import pystray
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import traceback
import sys

sys.stdout.reconfigure(encoding='utf-8')

def show_error(title, message):
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title, message)
    root.destroy()

def load_settings():
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        else:
            default = {
                "muted": False,
                "autostart": False,
                "theme": "light",
                "notification_frequency_minutes": 1,
                "notification_duration": 8,
                "notification_types": ["eye", "hydration", "stretch"],
                "quote_tone": "humorous",
                "notification_position": "bottom-right",
                "custom_message": "",
                "animation": {
                    "eye": "assets/blink_eyes.gif",
                    "hydration": "assets/water_bottle.gif"
                }
            }
            with open('config.json', 'w') as f:
                json.dump(default, f, indent=4)
            return default
    except Exception as e:
        show_error("Settings Error", f"Error loading settings: {str(e)}")
        return {}

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning! 🌞", "Start your day with a smile and energy!"
    elif 12 <= hour < 18:
        return "Good afternoon! ☀️", "Keep shining and make the most of the day!"
    else:
        return "Good evening! 🌙", "Time to unwind and reflect on a productive day!"

quotes = {
    "eye": "Look away from the screen and relax your eyes. Time for a little break!",
    "hydration": "Stay hydrated and feel your best - grab a glass of water and refresh yourself! 💧",
    "stretch": "Take a deep breath, stretch your body, and feel refreshed for a productive day ahead!"
}

class SoukyaApp:
    def __init__(self):
        try:
            print("Initializing Soukya application")
            self.settings = load_settings()
            self.notifier = Notifier(self.settings)
            self.icon = self.create_tray_icon()
            self.settings_window = None
        except Exception as e:
            show_error("Initialization Error", f"Error initializing application: {str(e)}\n{traceback.format_exc()}")
            sys.exit(1)

    def create_tray_icon(self):
        try:
            icon_image = Image.new('RGB', (64, 64), color=(73, 109, 137))
            draw = ImageDraw.Draw(icon_image)
            draw.ellipse([4, 4, 60, 60], fill=(73, 109, 137), outline=(255, 255, 255), width=2)

            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            draw.text((22, 12), "S", fill=(255, 255, 255), font=font)

            def on_settings():
                if self.settings_window is None or not self.settings_window.window.winfo_exists():
                    self.settings_window = SettingsWindow(self.notifier.root)
                    self.settings_window.window.protocol("WM_DELETE_WINDOW", self.on_settings_close)
                else:
                    self.settings_window.window.lift()
                    self.settings_window.window.focus_force()

            def on_exit():
                self.icon.stop()
                os._exit(0)

            icon = pystray.Icon("Soukya", icon_image, "Soukya - Wellness Notifier", menu=pystray.Menu(
                pystray.MenuItem("Open Settings", on_settings),
                pystray.MenuItem("Exit", on_exit)
            ))

            threading.Thread(target=lambda: time.sleep(1), daemon=True).start()
            return icon
        except Exception as e:
            show_error("Tray Icon Error", f"Error creating tray icon: {str(e)}\n{traceback.format_exc()}")
            sys.exit(1)

    def on_settings_close(self):
        if self.settings_window and self.settings_window.window.winfo_exists():
            self.settings_window.window.destroy()
        self.settings_window = None

    def show_initial_notifications(self):
        try:
            print("Showing initial notifications")
            title, message = get_greeting()
            self.notifier.show_notification(title, message, "greeting")

            def show_test_notifications():
                print("Starting test notifications")
                time.sleep(10)
                self.notifier.show_notification("Look Away", quotes["eye"], "eye")
                time.sleep(20)
                self.notifier.show_notification("Hydration Break", quotes["hydration"], "hydration")
                time.sleep(20)
                self.notifier.show_notification("Stretch & Breathe", quotes["stretch"], "stretch")

            threading.Thread(target=show_test_notifications, daemon=True).start()
        except Exception as e:
            show_error("Notification Error", f"Error showing notifications: {str(e)}\n{traceback.format_exc()}")

    def run(self):
        try:
            print("Starting Soukya application")
            self.show_initial_notifications()
            threading.Thread(target=self.icon.run, daemon=True).start()
            self.notifier.run()
        except Exception as e:
            show_error("Runtime Error", f"Error running application: {str(e)}\n{traceback.format_exc()}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        app = SoukyaApp()
        app.run()
    except Exception as e:
        show_error("Fatal Error", f"Application failed to start: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1)
