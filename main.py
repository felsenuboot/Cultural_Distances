# %%
import json
import os
import pandas as pd
from scipy.spatial.distance import pdist, squareform
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from sklearn.cluster import KMeans
import numpy as np
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter

# %%
def clear_terminal():
    """Clear the terminal output."""
    os.system('cls' if os.name == 'nt' else 'clear')

# %%
def calculate_scaled_euclidean_distances(data, score_key="scores"):
    # Extract country names and scores
    countries = [item["name"] for item in data]
    scores = [item[score_key] for item in data]
    
    # Convert scores to a DataFrame
    scores_df = pd.DataFrame(scores, index=countries).replace(-1, pd.NA).dropna(axis=1, how="any")
    
    # Calculate variances for scaled Euclidean distance
    variances = scores_df.var().values
    
    # Calculate pairwise distances using scaled Euclidean distance
    distances = pdist(scores_df, metric="seuclidean", V=variances)
    
    # Convert distances to a squareform matrix and create a DataFrame for readability
    distance_matrix = squareform(distances)
    distance_df = pd.DataFrame(distance_matrix, index=countries, columns=countries)
    
    return distance_df

# %%
def visualize_country_network(distance_df, selected_countries=None, title="Network Graph of Country Distances", show=False):
    """
    Visualize a network graph of country distances to scale.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
        selected_countries (list): A list of country codes to include in the graph. If None, include all countries.
        title (str): Title of the graph.
    """
    # Use all countries if no selection is provided
    if selected_countries is None:
        selected_countries = distance_df.index.tolist()
    
    # Filter the distance matrix for the selected countries
    filtered_df = distance_df.loc[selected_countries, selected_countries]
    
    # Use MDS to compute positions to scale
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    positions = mds.fit_transform(filtered_df.values)
    
    # Map positions to a dictionary for NetworkX
    pos = {country: (positions[i, 0], positions[i, 1]) for i, country in enumerate(filtered_df.index)}
    
    # Create a network graph
    G = nx.Graph()
    
    # Add edges with weights
    for country1 in filtered_df.index:
        for country2 in filtered_df.columns:
            if country1 != country2:  # Avoid self-loops
                G.add_edge(country1, country2, weight=filtered_df.loc[country1, country2])
    
    # Draw the network graph
    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="black")
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7, edge_color="black")
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="white")
    
    # Add edge labels to indicate distances
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}  # Format weights
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Turn off axes for a clean look
    plt.axis("off")

    # Show the plot
    plt.title(title)
    plt.savefig("figures/" + title + ".png", format='png', dpi=300)
    if(show):
        plt.show()

# %%
def plot_kmeans_with_highlight(distance_df, highlight_countries, n_clusters=4, title="K-Means Clustering with Highlighted Countries", show=False):
    """
    Plot a K-Means clustering result with MDS coordinates, highlighting specific countries.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
        highlight_countries (list): List of country names to highlight in the plot.
        n_clusters (int): Number of clusters for K-Means.
        title (str): Title of the plot.
    """
    # Perform MDS to reduce the distance matrix to 2D coordinates
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    mds_coordinates = mds.fit_transform(distance_df.values)
    
    # Perform K-Means clustering on the distance matrix
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_labels = kmeans.fit_predict(distance_df)
    
    # Scatter plot of MDS coordinates
    plt.figure(figsize=(12, 8))
    plt.scatter(mds_coordinates[:, 0], mds_coordinates[:, 1], c=kmeans_labels, cmap='viridis', s=100, label="Clustered Points")
    
    # Annotate and highlight specific countries
    for i, country in enumerate(distance_df.index):
        if country in highlight_countries:
            plt.scatter(
                mds_coordinates[i, 0], 
                mds_coordinates[i, 1], 
                color='red', 
                s=200, 
                edgecolor='black', 
                label=f"Highlighted: {country}" if i == 0 else None
            )
            plt.annotate(
                country, 
                (mds_coordinates[i, 0] + 0.1, mds_coordinates[i, 1] + 0.1),
                fontsize=12,
                fontweight='bold',
                color='white',
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='black')
            )
        else:
            plt.annotate(
                country,
                (mds_coordinates[i, 0] + 0.05, mds_coordinates[i, 1] + 0.05),
                fontsize=8,
                color='black'
            )
    
    # Title and labels
    plt.title(title)
    plt.xlabel('MDS Dimension 1')
    plt.ylabel('MDS Dimension 2')
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/" + title + ".png", format='png', dpi=300)
    if(show):
        plt.show()

# %%
def dynamic_country_selection(prompt_message, countries):
    """
    Use fuzzy search with autocompletion for country selection.

    Args:
        prompt_message (str): Prompt message for the user.
        countries (list): List of available countries.

    Returns:
        str: Selected country.
    """
    completer = FuzzyCompleter(WordCompleter(countries, ignore_case=True))
    while True:
        country = prompt(f"{prompt_message}: ", completer=completer).strip()
        if country in countries:
            return country
        print("Invalid selection. Please try again.")

# %%
def extract_distance(distance_df):
    """
    Extract the distance of a country pair through a selection menu.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
    """
    print("\n--- Country Distance Extraction Menu ---")
    countries = distance_df.index.tolist()
    
    country1 = dynamic_country_selection("Select the first country", countries)
    country2 = dynamic_country_selection("Select the second country", countries)
    
    distance = distance_df.loc[country1, country2]
    print(f"\nDistance between {country1} and {country2}: {distance:.2f}")

# %%
def export_distances_to_csv(distance_df, title):
    clear_terminal()
    print("\n--- Export Distances to CSV ---")
    filename = f"{title.replace(' ', '_').lower()}_distances.csv"
    try:
        distance_df.to_csv("data/" + filename)
        print(f"Distances successfully exported to {filename}")
    except Exception as e:
        print(f"Error exporting distances: {e}")

def find_max_min_distances(distance_df):
    """
    Find and display the maximum and minimum distances between countries.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
    """
    # Get the maximum and minimum distances (ignore diagonal elements which are zero)
    max_distance = distance_df.where(~np.eye(distance_df.shape[0], dtype=bool)).max().max()
    min_distance = distance_df.where(~np.eye(distance_df.shape[0], dtype=bool)).min().min()

    # Find the corresponding countries for max distance
    max_location = distance_df.where(distance_df == max_distance).stack().idxmax()
    min_location = distance_df.where(distance_df == min_distance).stack().idxmin()

    print(f"Maximum distance: {max_distance:.2f} between {max_location[0]} and {max_location[1]}")
    print(f"Minimum distance: {min_distance:.2f} between {min_location[0]} and {min_location[1]}")

def find_max_min_distances_for_country(title, distance_df, country):
    """
    Find the maximum and minimum distances for a specific country.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
        country (str): The country for which to find max and min distances.
    """
    if country not in distance_df.index:
        print(f"Country '{country}' not found in the dataset.")
        return

    # Exclude the self-distance (diagonal)
    distances = distance_df.loc[country].drop(country)

    # Find maximum and minimum distances
    max_distance = distances.max()
    min_distance = distances.min()

    # Get corresponding countries
    max_country = distances.idxmax()
    min_country = distances.idxmin()

    print(f"{title}: The distances for {country} are...")
    print(f"  Maximum distance: {max_distance:.2f} with {max_country}")
    print(f"  Minimum distance: {min_distance:.2f} with {min_country}")
# %%
def main():
    with open("data/hofstede_data.json", "r") as f:
        hofstede_data = json.load(f)
    with open("data/culture_map_data.json", "r") as f:
        culture_map_data = json.load(f)

    while True:
        clear_terminal()
        print("\n--- Main Menu ---")
        print("1. Use Hofstede Data")
        print("2. Use Culture Map Data")
        print("3. Exit")
        data_choice = input("Select an option (1-3): ").strip()

        if data_choice == "1":
            data = hofstede_data
            selected_countries = ["Germany", "Great Britain", "Indonesia", "Ireland", "Japan", "U.S.A."]
            title = "Hofstede Data"
        elif data_choice == "2":
            data = culture_map_data
            selected_countries = ["Germany", "UK", "Indonesia", "Ireland", "Japan", "United States"]
            title = "Culture Map Data"
        elif data_choice == "3":
            print("Exiting.")
            break
        else:
            clear_terminal()
            print("Exiting")
            clear_terminal()
            break
            print("Invalid choice. Try again.")
            continue

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
            print("7. Return to Main Menu")
            choice = input("Select an option (1-7): ").strip()

            if choice == "1":
                extract_distance(distance_df)
                input("\nPress Enter to return to the submenu...")
            elif choice == "2":
                visualize_country_network(distance_df, title=f"{title}: Network Graph")
                input("\nGraph generated. Press Enter to return to the submenu...")
            elif choice == "3":
                plot_kmeans_with_highlight(distance_df, selected_countries, title=f"{title}: K-Means Clustering")
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
                break
            else:
                break
                print("Invalid choice. Try again.")

# %%
if __name__ == "__main__":
    main()

