# main.py
import argparse
import json
from terminal import terminal_interface

def main():
    parser = argparse.ArgumentParser(description="Cultural Dimensions Application")
    parser.add_argument("-t", "--terminal", action="store_true", help="Launch terminal interface")
    args = parser.parse_args()

    with open("data/hofstede_data.json", "r") as f:
        hofstede_data = json.load(f)
    
    with open("data/culture_map_data.json", "r") as f:
        culture_map_data = json.load(f)

    if args.terminal:
        while True:
            print("\n--- Main Menu ---")
            print("1. Use Hofstede Data")
            print("2. Use Culture Map Data")
            print("3. Exit")
            data_choice = input("Select an option (1-3): ").strip()

            if data_choice == "1":
                data = hofstede_data
                title = "Hofstede Data"
            elif data_choice == "2":
                data = culture_map_data
                title = "Culture Map Data"
            elif data_choice == "3":
                print("Exiting.")
                break
            else:
                break

            terminal_interface(data, title)

if __name__ == "__main__":
    main()
