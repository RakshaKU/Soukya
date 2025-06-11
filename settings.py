import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, time

class SettingsWindow:
    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Soukya Settings")
        self.window.geometry("500x700")  # Made window taller
        self.window.resizable(False, False)
        
        # Make window stay on top
        self.window.attributes('-topmost', True)
        
        # Load current settings
        self.settings = self.load_settings()
        
        # Set custom icon
        try:
            icon_img = tk.PhotoImage(file="assets/image.png")
            self.window.iconphoto(False, icon_img)
        except Exception as e:
            print(f"Could not set window icon: {e}")
        
        # Create main container with padding
        main_container = ttk.Frame(self.window, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create sections
        self.create_general_section(scrollable_frame)
        self.create_notification_section(scrollable_frame)
        self.create_custom_reminders_section(scrollable_frame)  # New section
        self.create_appearance_section(scrollable_frame)
        self.create_quotes_section(scrollable_frame)
        
        # Save and Cancel buttons
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def create_general_section(self, parent):
        # General Settings Section
        general_frame = ttk.LabelFrame(parent, text="General Settings", padding="10")
        general_frame.pack(fill=tk.X, pady=10)
        
        # Mute toggle
        self.muted_var = tk.BooleanVar(value=self.settings.get("muted", False))
        ttk.Checkbutton(general_frame, text="Mute All Notifications", variable=self.muted_var).pack(anchor=tk.W, pady=5)
        
        # Auto-start with Windows
        self.autostart_var = tk.BooleanVar(value=self.settings.get("autostart", False))
        ttk.Checkbutton(general_frame, text="Start with Windows", variable=self.autostart_var).pack(anchor=tk.W, pady=5)
    
    def create_notification_section(self, parent):
        # Notification Settings Section
        notification_frame = ttk.LabelFrame(parent, text="Notification Settings", padding="10")
        notification_frame.pack(fill=tk.X, pady=10)
        
        # Notification frequency
        ttk.Label(notification_frame, text="Notification Frequency (minutes):").pack(anchor=tk.W, pady=5)
        self.frequency_var = tk.IntVar(value=self.settings.get("notification_frequency_minutes", 30))
        frequency_entry = ttk.Entry(notification_frame, textvariable=self.frequency_var, width=10)
        frequency_entry.pack(anchor=tk.W, pady=5)
        
        # Notification duration
        ttk.Label(notification_frame, text="Notification Display Duration (seconds):").pack(anchor=tk.W, pady=5)
        self.duration_var = tk.IntVar(value=self.settings.get("notification_duration", 8))
        duration_entry = ttk.Entry(notification_frame, textvariable=self.duration_var, width=10)
        duration_entry.pack(anchor=tk.W, pady=5)
        
        # Notification types
        ttk.Label(notification_frame, text="Enable Notification Types:").pack(anchor=tk.W, pady=5)
        self.eye_var = tk.BooleanVar(value="eye" in self.settings.get("notification_types", []))
        self.hydration_var = tk.BooleanVar(value="hydration" in self.settings.get("notification_types", []))
        self.stretch_var = tk.BooleanVar(value="stretch" in self.settings.get("notification_types", []))
        
        ttk.Checkbutton(notification_frame, text="Eye Relaxation Reminders", variable=self.eye_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(notification_frame, text="Hydration Reminders", variable=self.hydration_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(notification_frame, text="Stretch Reminders", variable=self.stretch_var).pack(anchor=tk.W, pady=2)
    
    def create_custom_reminders_section(self, parent):
        # Custom Reminders Section
        reminders_frame = ttk.LabelFrame(parent, text="Custom Reminders", padding="10")
        reminders_frame.pack(fill=tk.X, pady=10)
        
        # List of current reminders
        ttk.Label(reminders_frame, text="Your Reminders:").pack(anchor=tk.W, pady=5)
        
        # Create a frame for the listbox and scrollbar
        list_frame = ttk.Frame(reminders_frame)
        list_frame.pack(fill=tk.X, pady=5)
        
        # Create listbox for reminders
        self.reminders_listbox = tk.Listbox(list_frame, height=4)
        self.reminders_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add scrollbar to listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.reminders_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.reminders_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Load existing reminders into listbox
        self.custom_reminders = self.settings.get("custom_reminders", [])
        for reminder in self.custom_reminders:
            self.reminders_listbox.insert(tk.END, f"{reminder['title']} - {reminder['days']} at {reminder['time']}")
        
        # Frame for adding new reminders
        add_frame = ttk.LabelFrame(reminders_frame, text="Add New Reminder", padding="10")
        add_frame.pack(fill=tk.X, pady=10)
        
        # Reminder title
        ttk.Label(add_frame, text="Reminder Title:").pack(anchor=tk.W, pady=2)
        self.reminder_title = ttk.Entry(add_frame, width=40)
        self.reminder_title.pack(anchor=tk.W, pady=2)
        
        # Days selection
        ttk.Label(add_frame, text="Days:").pack(anchor=tk.W, pady=2)
        days_frame = ttk.Frame(add_frame)
        days_frame.pack(fill=tk.X, pady=2)
        
        self.day_vars = {}
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            var = tk.BooleanVar()
            self.day_vars[day] = var
            ttk.Checkbutton(days_frame, text=day, variable=var).pack(side=tk.LEFT, padx=2)
        
        # Time selection
        ttk.Label(add_frame, text="Time:").pack(anchor=tk.W, pady=2)
        time_frame = ttk.Frame(add_frame)
        time_frame.pack(fill=tk.X, pady=2)
        
        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")
        self.ampm_var = tk.StringVar(value="AM")
        
        # Hour dropdown
        hours = [f"{i:02d}" for i in range(1, 13)]
        ttk.Combobox(time_frame, textvariable=self.hour_var, values=hours, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT)
        
        # Minute dropdown
        minutes = [f"{i:02d}" for i in range(0, 60, 5)]
        ttk.Combobox(time_frame, textvariable=self.minute_var, values=minutes, width=3).pack(side=tk.LEFT, padx=2)
        
        # AM/PM dropdown
        ttk.Combobox(time_frame, textvariable=self.ampm_var, values=["AM", "PM"], width=3).pack(side=tk.LEFT, padx=2)
        
        # Add and Remove buttons
        button_frame = ttk.Frame(add_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Add Reminder", command=self.add_reminder).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_reminder).pack(side=tk.LEFT, padx=2)
    
    def add_reminder(self):
        """Add a new custom reminder"""
        title = self.reminder_title.get().strip()
        selected_days = [day for day, var in self.day_vars.items() if var.get()]
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        ampm = self.ampm_var.get()
        
        # Validate inputs
        if not title:
            messagebox.showerror("Error", "Please enter a reminder title")
            return
        if not selected_days:
            messagebox.showerror("Error", "Please select at least one day")
            return
            
        # Format time
        time_str = f"{hour}:{minute} {ampm}"
        
        # Create reminder
        reminder = {
            "title": title,
            "days": selected_days,
            "time": time_str
        }
        
        # Add to listbox and settings
        self.reminders_listbox.insert(tk.END, f"{title} - {', '.join(selected_days)} at {time_str}")
        self.settings["custom_reminders"].append(reminder)
        
        # Save settings
        self.save_settings()
        
        # Clear inputs
        self.reminder_title.delete(0, tk.END)
        for var in self.day_vars.values():
            var.set(False)
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.ampm_var.set("AM")
        
        print(f"Added new reminder: {reminder}")  # Debug print
    
    def remove_reminder(self):
        """Remove selected reminder"""
        selection = self.reminders_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a reminder to remove")
            return
            
        index = selection[0]
        reminder = self.settings["custom_reminders"][index]
        
        # Remove from listbox and settings
        self.reminders_listbox.delete(index)
        self.settings["custom_reminders"].pop(index)
        
        # Save settings
        self.save_settings()
        
        print(f"Removed reminder: {reminder}")  # Debug print
    
    def create_appearance_section(self, parent):
        # Appearance Settings Section
        appearance_frame = ttk.LabelFrame(parent, text="Appearance", padding="10")
        appearance_frame.pack(fill=tk.X, pady=10)
        
        # Theme selection
        ttk.Label(appearance_frame, text="Theme:").pack(anchor=tk.W, pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        theme_combo = ttk.Combobox(appearance_frame, textvariable=self.theme_var, values=["light", "dark", "system"])
        theme_combo.pack(anchor=tk.W, pady=5)
        
        # Notification position
        ttk.Label(appearance_frame, text="Notification Position:").pack(anchor=tk.W, pady=5)
        self.position_var = tk.StringVar(value=self.settings.get("notification_position", "bottom-right"))
        position_combo = ttk.Combobox(appearance_frame, textvariable=self.position_var, 
                                    values=["top-right", "top-left", "bottom-right", "bottom-left"])
        position_combo.pack(anchor=tk.W, pady=5)
    
    def create_quotes_section(self, parent):
        # Quotes Settings Section
        quotes_frame = ttk.LabelFrame(parent, text="Quotes & Messages", padding="10")
        quotes_frame.pack(fill=tk.X, pady=10)
        
        # Quote tone
        ttk.Label(quotes_frame, text="Message Tone:").pack(anchor=tk.W, pady=5)
        self.quote_tone_var = tk.StringVar(value=self.settings.get("quote_tone", "humorous"))
        quote_tone_combo = ttk.Combobox(quotes_frame, textvariable=self.quote_tone_var, 
                                      values=["humorous", "motivational", "minimal", "professional"])
        quote_tone_combo.pack(anchor=tk.W, pady=5)
        
        # Custom message
        ttk.Label(quotes_frame, text="Custom Message (optional):").pack(anchor=tk.W, pady=5)
        self.custom_message_var = tk.StringVar(value=self.settings.get("custom_message", ""))
        custom_message_entry = ttk.Entry(quotes_frame, textvariable=self.custom_message_var, width=40)
        custom_message_entry.pack(anchor=tk.W, pady=5)
    
    def load_settings(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        return {}
    
    def save_settings(self):
        """Save settings to config file"""
        try:
            # Update all settings before saving
            self.settings.update({
                "muted": self.muted_var.get(),
                "autostart": self.autostart_var.get(),
                "theme": self.theme_var.get(),
                "notification_frequency_minutes": self.frequency_var.get(),
                "notification_duration": self.duration_var.get(),
                "notification_types": [
                    "eye" if self.eye_var.get() else None,
                    "hydration" if self.hydration_var.get() else None,
                    "stretch" if self.stretch_var.get() else None
                ],
                "quote_tone": self.quote_tone_var.get(),
                "notification_position": self.position_var.get(),
                "custom_message": self.custom_message_var.get(),
                "custom_reminders": self.settings.get("custom_reminders", [])  # Preserve custom reminders
            })
            
            # Remove None values from notification_types
            self.settings["notification_types"] = [t for t in self.settings["notification_types"] if t is not None]
            
            with open('config.json', 'w') as f:
                json.dump(self.settings, f, indent=4)
            print("Settings saved successfully")  # Debug print
            print(f"Custom reminders saved: {self.settings.get('custom_reminders', [])}")  # Debug print
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            print(f"Error saving settings: {str(e)}")  # Debug print
        
        self.window.destroy()
    
    def run(self):
        self.window.mainloop()