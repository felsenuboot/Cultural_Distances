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

def clear_terminal():
    """Clear the terminal output."""
    os.system('cls' if os.name == 'nt' else 'clear')

def dynamic_country_selection(prompt_message, countries, allow_empty=False):
    """
    Use fuzzy search with autocompletion for country selection.
    """
    completer = FuzzyCompleter(WordCompleter(countries, ignore_case=True))
    while True:
        country = prompt(f"{prompt_message}: ", completer=completer).strip()
        if allow_empty and country == "":
            return None
        if country in countries:
            return country
        print("Invalid selection. Please try again.")

def extract_distance(distance_df):
    """Extract the distance of a country pair through a selection menu."""
    print("\n--- Country Distance Extraction Menu ---")
    countries = distance_df.index.tolist()
    
    country1 = dynamic_country_selection("Select the first country", countries)
    country2 = dynamic_country_selection("Select the second country", countries)
    
    distance = distance_df.loc[country1, country2]
    print(f"\nDistance between {country1} and {country2}: {distance:.2f}")

def terminal_interface(data, title):
    distance_df = calculate_scaled_euclidean_distances(data)

    while True:
        clear_terminal()
        print(f"\n--- Submenu: {title} ---")
        print("1. Extract Distance")
        print("2. Visualize Network")
        print("3. Visualize K-Means Clustering")
        print("4. Export Distances to CSV")
        print("5. Find Maximum and Minimum Distances")
        print("6. Find Max/Min Distances for a Specific Country")
        print("7. Box Plot with Highlighted Distances")
        print("8. Return to Main Menu")
        choice = input("Select an option (1-8): ").strip()

        if choice == "1":
            extract_distance(distance_df)
            input("\nPress Enter to return to the submenu...")
        elif choice == "2":
            visualize_country_network(distance_df, title=f"{title} - Network Graph")
            input("\nGraph generated. Press Enter to return to the submenu...")
        elif choice == "3":
            plot_kmeans_with_highlight_t_SNE(distance_df, [], title=f"{title} - K-Means Clustering (t-SNE)")
            plot_kmeans_with_highlight_MDS(distance_df, [], title=f"{title} - K-Means Clustering (MDS)")
            input("\nCluster visualization complete. Press Enter to return to the submenu...")
        elif choice == "4":
            export_distances_to_csv(distance_df, title)
            input("\nPress Enter to return to the submenu...")
        elif choice == "5":
            find_max_min_distances(distance_df)
            input("\nPress Enter to return to the submenu...")
        elif choice == "6":
            clear_terminal()
            country = dynamic_country_selection(f" {title} - Select a country", distance_df.index.tolist())
            clear_terminal()
            find_max_min_distances_for_country(title, distance_df, country)
            input("\nPress Enter to return to the submenu...")
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
            boxplot_with_highlight(distance_df, country, highlight_countries, title=title)
            input("\nBox plot generated. Press Enter to return to the submenu...")
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")
