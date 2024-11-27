# terminal.py
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from functions import (
    calculate_scaled_euclidean_distances, 
    visualize_country_network, 
    plot_kmeans_with_highlight_MDS, 
    plot_kmeans_with_highlight_t_SNE, 
    export_distances_to_csv, 
    find_max_min_distances, 
    find_max_min_distances_for_country, 
    boxplot_with_highlight
)

from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.progress import Progress
from rich.align import Align
from time import sleep
console = Console()


def clear_terminal():
    """Clear the terminal output."""
    os.system('cls' if os.name == 'nt' else 'clear')

def dynamic_country_selection(prompt_message, countries, allow_empty=False):
    """
    Use fuzzy search with autocompletion for country selection.
    """
    completer = FuzzyCompleter(WordCompleter(countries, ignore_case=True))
    while True:
        # Display the prompt message with rich
        console.print(
            Panel(
                Align.center(f"[bold cyan]{prompt_message}[/bold cyan]\n[italic white](Type a country name or press Enter to skip)[/italic white]"),
                border_style="cyan",
                padding=(1, 2)
            )
        )
        # Use a simple string prompt for input
        country = prompt("➡️  Your choice: ", completer=completer).strip()
        
        if allow_empty and country == "":
            return None
        if country in countries:
            return country
        
        # Display error message using rich
        console.print(Panel("[bold red]Invalid selection. Please try again.[/bold red]", border_style="red"))

def extract_distance(distance_df):
    """Extract the distance of a country pair through a selection menu."""
    console.print(
        Panel("[bold blue]Country Distance Extraction Menu[/bold blue]", border_style="blue", padding=(1, 2))
    )
    countries = distance_df.index.tolist()
    country1 = dynamic_country_selection("Select the first country", countries)
    clear_terminal()
    country2 = dynamic_country_selection(f"First Country: [blue] {country1} \n[bold cyan]Select the second country", countries)
    distance = distance_df.loc[country1, country2]
    clear_terminal()
    console.print(
        Panel(f"[bold green]:sparkle: Distance between {country1} and {country2}: {distance:.2f} :sparkle: [/bold green][red]\n\n Press Enter to return to the submenu...", border_style="green", padding=1)
    )

def terminal_interface(data, title, show):
    console = Console()
    distance_df = calculate_scaled_euclidean_distances(data)
    
    if title == "Hofstede Data":
        selected_countries = ["Germany", "Great Britain", "Indonesia", "Ireland", "Japan", "U.S.A."]
    elif title == "Culture Map Data":
        selected_countries = ["Germany", "UK", "Indonesia", "Ireland", "Japan", "United States"]
        
    while True:
        clear_terminal()

        # Prepare menu entries
        entries= [
            "1. Extract Distance",
            "2. Visualize Network",
            "3. Visualize K-Means Clustering",
            "4. Export Distances to CSV",
            "5. Find Maximum and Minimum Distances",
            "6. Find Max/Min Distances for a Specific Country",
            "7. Box Plot with Highlighted Distances",
            "8. Return to Main Menu"
            ]
        user_renderables = [Panel(entry) for entry in entries]

        # Render the main menu
        menu_columns = Columns(user_renderables, equal=True, expand=True)
        menu_panel = Panel(Align.center(menu_columns), title=f"Submenu: {title}", padding=(1, 2))

        console.print(menu_panel)

        choice = input("Select an option (1-8): ").strip()

        if choice == "1":
            clear_terminal()
            extract_distance(distance_df)
            input()
        elif choice == "2":
            clear_terminal()
            visualize_country_network(distance_df, selected_countries, title=f"{title} - Network Graph", show=show)
            console.print(
                Panel(f"[bold green]:sparkle: Graph generated. :sparkle: [/bold green][red]\n\n Press Enter to return to the submenu...", border_style="green", padding=1)
            )
            input()
        elif choice == "3":
            clear_terminal()
            progress = Progress(auto_refresh=True)
            master_task = progress.add_task("overall", total=3)  # Two tasks: t-SNE and MDS

            progress.console.print(
                Panel(
                    "[bold blue]Generating cluster visualizations with t-SNE and MDS...",
                    padding=1,
                )
            )

            with progress:
                # t-SNE Visualization Task
                progress.log("[bold yellow]Starting t-SNE visualization...")
                progress.update(master_task, advance=1, description="Running t-SNE")
                plot_kmeans_with_highlight_t_SNE(distance_df, selected_countries, title=f"{title} - K-Means Clustering (t-SNE)", show=show)
                sleep(1)  # Simulating progress
                progress.log("[green]t-SNE visualization complete.")

                # MDS Visualization Task
                progress.log("[bold yellow]Starting MDS visualization...")
                progress.update(master_task, advance=1, description="Running MDS")
                plot_kmeans_with_highlight_MDS(distance_df, selected_countries, title=f"{title} - K-Means Clustering (MDS)",show=show)
                sleep(1)  # Simulating progress
                progress.log("[green]MDS visualization complete.")
                progress.update(master_task, advance=1, description="complete")
            progress.console.print(
                Panel("[bold green]:sparkle: Cluster visualization complete! :sparkle: [red]\n\n Press Enter to return to the submenu...", border_style="green", padding=1)
            )
            input()
        elif choice == "4":
            clear_terminal()
            filename = export_distances_to_csv(distance_df, title)
            console.print(
                Panel(f"[bold green]:sparkle: Distances successfully exported to {filename} :sparkle: [/bold green][red]\n\n Press Enter to return to the submenu...", border_style="green", padding=1)
            )
            input()
        elif choice == "5":
            clear_terminal()
            max, min = find_max_min_distances(distance_df)
            panel = Panel(Align.center(f"[bold green]:sparkle: {max} :sparkle:\n:sparkle: {min} :sparkle:[/bold green][red]\n\n Press Enter to return to the submenu..."), title=f"Distances for: {title}", padding=(1, 2))
            console.print(panel)
            input()
        elif choice == "6":
            clear_terminal()
            country = dynamic_country_selection(f" {title} - Select a country", distance_df.index.tolist())
            clear_terminal()
            max, min= find_max_min_distances_for_country(title, distance_df, country)
            
            panel = Panel(Align.center(f"[bold green]:sparkle: {max} :sparkle:\n:sparkle: {min} :sparkle:[/bold green][red]\n\n Press Enter to return to the submenu..."), title=f"Distances for: {country}", padding=(1, 2))
            console.print(panel)
            input()
        elif choice == "7":
            clear_terminal()
            country = dynamic_country_selection(f" {title} - Select a country", distance_df.index.tolist())
            if not country:
                print("No country selected. Returning to submenu.")
                continue

            highlight_countries = []
            print("\nSelect countries to highlight (press Enter with no input to finish):")
            while True:
                highlight = dynamic_country_selection("Select a country to highlight", distance_df.index.tolist(), allow_empty=True)
                if not highlight:
                    break
                highlight_countries.append(highlight)
                print(f"Added {highlight} to highlights.")
            boxplot_with_highlight(distance_df, country, highlight_countries, title=title,show=show)
            clear_terminal()
            console.print(
                Panel(f"[bold green]:sparkle: Box plot generated. :sparkle: [/bold green][red]\n\n Press Enter to return to the submenu...", border_style="green", padding=1)
            )
            input()
        elif choice == "8":
            break
        else:
            break
    clear_terminal()
