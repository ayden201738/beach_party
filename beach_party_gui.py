#!/usr/bin/env python3
"""
Beach Party GUI Application
A simple graphical version of the beach party CLI app using tkinter
"""

import random
import json
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# Party details
PARTY = {
    "date": "July 15, 2026",
    "location": "Sandy Shores Beach",
    "theme": "Tropical Luau",
    "start_time": "2:00 PM",
    "end_time": "8:00 PM"
}

# Party points for tracking fun
party_points = 0

# Base points for each activity per weather condition
ACTIVITY_POINTS = {
    "swim": {
        "sunny": 10,
        "cloudy": 7,
        "rainy": 2,
        "windy": 4
    },
    "volleyball": {
        "sunny": 12,
        "cloudy": 9,
        "rainy": 1,
        "windy": 3
    },
    "bbq": {
        "sunny": 15,
        "cloudy": 11,
        "rainy": 0,
        "windy": 5
    }
}

# Guest file for persistent storage
GUEST_FILE = "beach_party_guests.json"

# Guest list (in-memory)
guests = []

# Activities and their outcomes based on weather
ACTIVITIES = {
    "swim": {
        "sunny": "The water is perfect for a refreshing swim! 🌊",
        "cloudy": "It's a bit overcast, but still nice for a swim. ⛅",
        "rainy": "Too rainy for swimming. Better stay dry! ☔",
        "windy": "Windy conditions make swimming challenging. 🌬️"
    },
    "volleyball": {
        "sunny": "Perfect volleyball weather! Set, spike, and score! 🏐",
        "cloudy": "Good light for volleyball without too much sun. 🏐",
        "rainy": "The court is wet and slippery. Postpone the game. 🌧️",
        "windy": "Wind is affecting the ball's trajectory. Play carefully! 💨"
    },
    "bbq": {
        "sunny": "Ideal BBQ weather! Grill those burgers and veggies! 🍔",
        "cloudy": "Great BBQ weather - not too hot. 🍔",
        "rainy": "Rain ruined the BBQ. Move indoors or cancel. ☔",
        "windy": "Wind is blowing smoke everywhere. Be careful with the grill! 🌬️"
    }
}

WEATHER_OPTIONS = ["sunny", "cloudy", "rainy", "windy"]


def load_guests():
    """Load guests from the persistent storage file."""
    global guests
    if os.path.exists(GUEST_FILE):
        try:
            with open(GUEST_FILE, 'r') as f:
                guests = json.load(f)
        except (json.JSONDecodeError, IOError):
            guests = []
    else:
        guests = []


def save_guests():
    """Save guests to the persistent storage file."""
    try:
        with open(GUEST_FILE, 'w') as f:
            json.dump(guests, f)
    except IOError:
        messagebox.showwarning("Warning", "Could not save guest list.")


def simulate_weather():
    """Return a random weather condition."""
    return random.choice(WEATHER_OPTIONS)


class BeachPartyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Beach Party CLI Application 🏖️")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Load guests
        load_guests()
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(main_frame, text="Welcome to the Beach Party!", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_details_tab()
        self.create_activities_tab()
        self.create_guests_tab()
        
        # Exit button
        exit_button = ttk.Button(main_frame, text="Exit", command=self.exit_app)
        exit_button.grid(row=2, column=0, pady=(10, 0))
        
    def create_details_tab(self):
        """Create the party details tab."""
        details_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(details_frame, text="Party Details")
        
        # Party details text
        details_text = tk.Text(details_frame, wrap=tk.WORD, height=10, width=50)
        details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for text
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=details_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        details_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        
        # Display party details
        details_content = "=== Beach Party Details ===\n\n"
        for key, value in PARTY.items():
            details_content += f"{key.capitalize().replace('_', ' ')}: {value}\n"
        details_content += f"\nParty Points: {party_points}\n"
        details_content += "\n" + "=" * 26 + "\n"
        
        details_text.insert(tk.END, details_content)
        details_text.configure(state=tk.DISABLED)  # Make read-only
        
    def create_activities_tab(self):
        """Create the activities tab."""
        activities_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(activities_frame, text="Activities")
        
        # Instructions
        instructions = ttk.Label(activities_frame, text="Choose an activity to see how the weather affects it:")
        instructions.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Activity buttons
        activities = [("Swim", "swim"), ("Volleyball", "volleyball"), ("BBQ", "bbq")]
        for i, (text, activity_key) in enumerate(activities):
            btn = ttk.Button(activities_frame, text=text, 
                           command=lambda key=activity_key: self.do_activity(key))
            btn.grid(row=i+1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Back button
        back_btn = ttk.Button(activities_frame, text="Back to Main Menu", 
                            command=lambda: self.notebook.select(0))
        back_btn.grid(row=len(activities)+1, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        
        # Result display
        self.activity_result = tk.Text(activities_frame, wrap=tk.WORD, height=6, width=40)
        self.activity_result.grid(row=0, column=2, rowspan=len(activities)+2, 
                                 padx=(20, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for result
        result_scrollbar = ttk.Scrollbar(activities_frame, orient=tk.VERTICAL, 
                                       command=self.activity_result.yview)
        result_scrollbar.grid(row=0, column=3, rowspan=len(activities)+2, 
                            sticky=(tk.N, tk.S))
        self.activity_result.configure(yscrollcommand=result_scrollbar.set)
        
        # Configure grid weights
        activities_frame.columnconfigure(0, weight=1)
        activities_frame.columnconfigure(2, weight=1)
        activities_frame.rowconfigure(len(activities)+1, weight=1)
        
    def create_guests_tab(self):
        """Create the guests management tab."""
        guests_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(guests_frame, text="Guest Management")
        
        # Instructions
        instructions = ttk.Label(guests_frame, text="Manage your guest list:")
        instructions.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Guest buttons
        button_frame = ttk.Frame(guests_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="Add Guest", 
                  command=self.add_guest).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Remove Guest", 
                  command=self.remove_guest).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="View Guest List", 
                  command=self.view_guests).grid(row=0, column=2, padx=(5, 0))
        
        # Guest list display
        self.guest_listbox = tk.Listbox(guests_frame, height=10, width=40)
        self.guest_listbox.grid(row=2, column=0, columnspan=2, 
                               sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Scrollbar for guest list
        guest_scrollbar = ttk.Scrollbar(guests_frame, orient=tk.VERTICAL, 
                                      command=self.guest_listbox.yview)
        guest_scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.guest_listbox.configure(yscrollcommand=guest_scrollbar.set)
        
        # Back button
        back_btn = ttk.Button(guests_frame, text="Back to Main Menu", 
                            command=lambda: self.notebook.select(0))
        back_btn.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Configure grid weights
        guests_frame.columnconfigure(0, weight=1)
        guests_frame.rowconfigure(2, weight=1)
        
        # Update guest list display
        self.update_guest_list()
        
    def do_activity(self, activity_key):
        """Perform an activity and show the result based on weather."""
        weather = simulate_weather()
        result = f"Current weather: {weather.capitalize()}\n\n"
        result += ACTIVITIES[activity_key][weather]
        
        # Calculate base points
        base_points = ACTIVITY_POINTS[activity_key][weather]
        
        # Apply guest bonus: +1 point per guest (up to 10 bonus points max)
        guest_bonus = min(len(guests), 10)
        total_points = base_points + guest_bonus
        
        # Update global party points
        global party_points
        party_points += total_points
        
        result += f"\n\nPoints Breakdown:\n"
        result += f"Base points: {base_points}\n"
        if guest_bonus > 0:
            result += f"Guest bonus: +{guest_bonus} points ({len(guests)} guests)\n"
        result += f"You earned {total_points} party points!\n"
        result += f"Total Party Points: {party_points}"
        
        # Clear and update result display
        self.activity_result.delete(1.0, tk.END)
        self.activity_result.insert(tk.END, result)
        
    def add_guest(self):
        """Add a guest to the list."""
        name = simpledialog.askstring("Add Guest", "Enter guest name:")
        if name and name.strip():
            name = name.strip()
            guests.append(name)
            self.update_guest_list()
            messagebox.showinfo("Success", f"Added {name} to the guest list.")
        elif name is not None:  # User clicked OK but entered empty string
            messagebox.showwarning("Input Error", "Name cannot be empty.")
            
    def remove_guest(self):
        """Remove a guest from the list."""
        selection = self.guest_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a guest to remove.")
            return
            
        index = selection[0]
        if 0 <= index < len(guests):
            removed = guests.pop(index)
            self.update_guest_list()
            messagebox.showinfo("Success", f"Removed {removed} from guest list.")
        else:
            messagebox.showerror("Error", "Invalid selection.")
            
    def view_guests(self):
        """View the guest list in a dialog."""
        if not guests:
            messagebox.showinfo("Guest List", "No guests added yet.")
            return
            
        guest_text = "\nGuest List:\n" + "-" * 20 + "\n"
        for i, guest in enumerate(guests, 1):
            guest_text += f"{i}. {guest}\n"
            
        messagebox.showinfo("Guest List", guest_text)
        
    def update_guest_list(self):
        """Update the guest listbox display."""
        self.guest_listbox.delete(0, tk.END)
        for guest in guests:
            self.guest_listbox.insert(tk.END, guest)
            
    def exit_app(self):
        """Exit the application."""
        save_guests()
        if messagebox.askokcancel("Exit", "Thanks for using the Beach Party GUI! Have a great day! 🌴"):
            self.root.quit()


def main():
    """Main application function."""
    root = tk.Tk()
    app = BeachPartyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()