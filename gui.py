# gui.py

import tkinter as tk
from tkinter import ttk
from data_processing import calculate_scaled_euclidean_distances

# GUI Launcher
def launch_gui(distance_df):
    app = tk.Tk()
    app.title("Country Distance Analysis")

    frame = ttk.Frame(app, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Select an action:").grid(row=0, column=0, sticky=tk.W)

    actions = {
        "Visualize Network": lambda: visualize_network_gui(distance_df),
    }

    for i, (action_name, action_func) in enumerate(actions.items()):
        ttk.Button(frame, text=action_name, command=action_func).grid(row=i+1, column=0, sticky=tk.W)

    app.mainloop()


def visualize_network_gui(distance_df):
    print("Network visualization through GUI is not yet implemented.")