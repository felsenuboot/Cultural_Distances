# main.py

import json
from data_processing import calculate_scaled_euclidean_distances
from terminal import display_terminal_menu
from gui import launch_gui

def load_data():
    with open("data/hofstede_data.json", "r") as f:
        hofstede_data = json.load(f)
    with open("data/culture_map_data.json", "r") as f:
        culture_map_data = json.load(f)
    return hofstede_data, culture_map_data

def main():
    hofstede_data, culture_map_data = load_data()

    while True:
        choice = display_terminal_menu(["Use Hofstede Data", "Use Culture Map Data", "Exit"], title="Main Menu")

        if choice == "1":
            data = hofstede_data
        elif choice == "2":
            data = culture_map_data
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")
            continue

        distance_df = calculate_scaled_euclidean_distances(data)

        interface_choice = display_terminal_menu(["Terminal Interface", "Graphical Interface (GUI)"]) 
        if interface_choice == "1":
            print("Terminal interaction not yet refactored.")
        elif interface_choice == "2":
            launch_gui(distance_df)

if __name__ == "__main__":
    main()