# main.py
import argparse
import json
from terminal import terminal_interface, clear_terminal, select_country_pairs
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from prompt_toolkit import prompt

from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.layout import Layout
from time import sleep

from functions import (
    calculate_scaled_euclidean_distances, 
    plot_two_distance_boxplots_with_highlight
    )

def display_fullscreen_exit_message(console, message):
    """Displays a fullscreen exit message centered both horizontally and vertically."""
    with console.screen():
        # Create a layout for fullscreen rendering
        layout = Layout()
        layout.split_column(
            Layout(Align.center(message, vertical="middle"), name="center")
        )

        # Wrap the centered content in a styled panel
        layout["center"].update(
            Panel(
                Align.center(message, vertical="middle"),
                title="Goodbye!",
                title_align="center",
                border_style="bold magenta",
                expand=True,
            )
        )

        # Render the layout
        console.print(layout)
        sleep(1)  # Hold the screen for 2 seconds before exiting

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
                "Use Hofstede Data",
                "Use Culture Map Data",
                "Box Plot all distances",
                "Exit"
            ]
            completer = FuzzyCompleter(WordCompleter(entries, ignore_case=True))

            user_renderables = [Panel(f'{i+1}. {entry}') for i, entry in enumerate(entries)]
            
            # Render the main menu
            menu_columns = Columns(user_renderables, equal=True, expand=True)
            menu_panel = Panel(Align.center(menu_columns), title="[bold blue]Main Menu[/bold blue]", padding=(1, 2))
            
            # Print the menu
            console.print(menu_panel)
            try:
                # Get user input
                data_choice = prompt("？ Select an option (1-3): ", completer=completer).strip()
                #data_choice = input("Select an option (1-3): ").strip()


                if data_choice == "1" or data_choice == entries[0]:
                    data = hofstede_data
                    title = "Hofstede Data"
                elif data_choice == "2" or data_choice == entries[1]:
                    data = culture_map_data
                    title = "Culture Map Data"
                elif data_choice == "3" or data_choice == entries[2]:
                    hs_distance_df = calculate_scaled_euclidean_distances(hofstede_data)
                    cm_distance_df = calculate_scaled_euclidean_distances(culture_map_data)
                    clear_terminal()
                    print("\nBox Plot of both frameworks with Highlighted Pairs")
                    
                    # Select country pairs for Hofstede framework
                    print("\n[bold blue]Select country pairs for the Hofstede framework:[/bold blue]")
                    highlighted_pairs_hofstede = select_country_pairs(hs_distance_df)

                    # Select country pairs for Culture Map framework
                    print("\n[bold blue]Select country pairs for the Culture Map framework:[/bold blue]")
                    highlighted_pairs_culture_map = select_country_pairs(cm_distance_df)
                    
                    # Combine pairs into a single dictionary for display
                    highlight_pairs = highlighted_pairs_hofstede + highlighted_pairs_culture_map

                    # Inform the user about selected pairs
                    console.print(
                        Panel(f"Selected pairs:\n\n[bold green]Hofstede:[/bold green] {highlighted_pairs_hofstede}\n[bold green]Culture Map:[/bold green] {highlighted_pairs_culture_map}",
                            title="[bold blue]Country Pairs for Highlighting[/bold blue]", border_style="blue", padding=1)
                    )
                    
                    # Check if any pairs are highlighted
                    if not highlighted_pairs_hofstede and not highlighted_pairs_culture_map:
                        print("No pairs selected. Generating boxplot without highlights...")
                    
                    # Plot the boxplot with or without highlighted pairs
                    plot_two_distance_boxplots_with_highlight(
                        hs_distance_df,
                        cm_distance_df, 
                        highlight_pairs=highlight_pairs, 
                        title=f"Both frameworks - Boxplot with Highlights", 
                        show=show
                    )
                    
                    console.print(
                        Panel(f"[bold green]:sparkle: Box plot generated. :sparkle: [/bold green][red]\n\nPress Enter to return to the submenu...", border_style="green", padding=1)
                    )
                    input()
                    break
                elif data_choice == "4" or data_choice == entries[2]:
                    display_fullscreen_exit_message(console, ":sparkle: Thank you for using the application! :sparkle: \nSee you next time.")
                    break
                else:
                    display_fullscreen_exit_message(console, ":sparkle: Thank you for using the application! :sparkle: \nSee you next time.")
                    break
                # Pass data to the terminal interface
                terminal_interface(data, title, show)
                clear_terminal()
            except KeyboardInterrupt:
                display_fullscreen_exit_message(console, "Keyboard Interrupt.\n\nExiting.")
                break


if __name__ == "__main__":
    main()
