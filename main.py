# main.py
import argparse
import json
from terminal import terminal_interface, clear_terminal
from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.align import Align

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="Cultural Dimensions Application")
    parser.add_argument("-t", "--terminal", action="store_true", help="Launch terminal interface")
    parser.add_argument("-s", "--show", action="store_true", help="Enable showing plots during execution")
    args = parser.parse_args()
    show = args.show


    with open("data/hofstede_data.json", "r") as f:
        hofstede_data = json.load(f)
    
    with open("data/culture_map_data.json", "r") as f:
        culture_map_data = json.load(f)

    if args.terminal:
        while True:
            clear_terminal()
            
            # Prepare menu entries
            entries = [
                "1. Use Hofstede Data",
                "2. Use Culture Map Data",
                "3. Exit"
            ]
            user_renderables = [Panel(entry) for entry in entries]
            
            # Render the main menu
            menu_columns = Columns(user_renderables, equal=True, expand=True)
            menu_panel = Panel(Align.center(menu_columns), title="Main Menu", padding=(1, 2))
            
            # Print the menu
            console.print(menu_panel)
            
            # Get user input
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

            # Pass data to the terminal interface
            terminal_interface(data, title, show)
            clear_terminal()
if __name__ == "__main__":
    main()
