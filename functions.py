
# Common styling for plots
PLOT_STYLE = {
    "node_color": "black",
    "node_size": 3000,
    "font_size": 8,
    "font_color": "white",
    "edge_color": "black",
    "figsize": (10, 7),
    "dpi": 300,
    "linewidth": 1.5,
    "boxprops": {"color": "black", "linewidth": 1.5},
    "whiskerprops": {"color": "black", "linewidth": 1.5},
    "capprops": {"color": "black", "linewidth": 1.5},
    "medianprops": {"color": "black", "linewidth": 1.5},
    "meanprops": {"color": "black", "linestyle": "--", "linewidth": 1.5},
    "highlight_color": "red",
    "highlight_size": 200,
}

# functions.py
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from sklearn.manifold import MDS, TSNE
from sklearn.cluster import KMeans
import networkx as nx

# Core Data Processing Functions
def calculate_scaled_euclidean_distances(data, score_key="scores"):
    countries = [item["name"] for item in data]
    scores = [item[score_key] for item in data]
    scores_df = pd.DataFrame(scores, index=countries).replace(-1, pd.NA).dropna(axis=1, how="any")
    variances = scores_df.var().values
    distances = pdist(scores_df, metric="seuclidean", V=variances)
    distance_matrix = squareform(distances)
    return pd.DataFrame(distance_matrix, index=countries, columns=countries)


def visualize_country_network(distance_df, selected_countries=None, title="Network Graph of Country Distances", show=False):
    """
    Visualize a network graph of country distances to scale.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
        selected_countries (list): A list of country codes to include in the graph. If None, include all countries.
        title (str): Title of the graph.
    """
    if selected_countries is None:
        selected_countries = distance_df.index.tolist()

    filtered_df = distance_df.loc[selected_countries, selected_countries]
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    positions = mds.fit_transform(filtered_df.values)
    pos = {country: (positions[i, 0], positions[i, 1]) for i, country in enumerate(filtered_df.index)}

    G = nx.Graph()
    for country1 in filtered_df.index:
        for country2 in filtered_df.columns:
            if country1 != country2:
                G.add_edge(country1, country2, weight=filtered_df.loc[country1, country2])

    plt.figure(figsize=PLOT_STYLE['figsize'])
    nx.draw_networkx_nodes(G, pos, node_size=PLOT_STYLE['node_size'], node_color=PLOT_STYLE['node_color'])
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7, edge_color=PLOT_STYLE['edge_color'])
    nx.draw_networkx_labels(G, pos, font_size=PLOT_STYLE['font_size'], font_color=PLOT_STYLE['font_color'])
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=PLOT_STYLE['font_size'])
    plt.axis("off")
    plt.title(title)
    plt.savefig(f"figures/{title}.png", format='png', dpi=300)
    if show:
        plt.show()


def plot_kmeans_with_highlight_MDS(distance_df, highlight_countries=[], n_clusters=4, title="K-Means Clustering with Highlighted Countries (MDS)", show=False):
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
    plt.savefig(f'figures/{title}.png', format='png', dpi=PLOT_STYLE['dpi'])
    if(show):
        plt.show()

def plot_kmeans_with_highlight_t_SNE(distance_df, highlight_countries=[], n_clusters=4, title="K-Means Clustering with Highlighted Countries (t-SNE)", show=False):
    """
    Plot a K-Means clustering result with t-SNE coordinates, highlighting specific countries.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
        highlight_countries (list): List of country names to highlight in the plot.
        n_clusters (int): Number of clusters for K-Means.
        title (str): Title of the plot.
    """
    # Perform t-SNE to reduce the distance matrix to 2D coordinates
    tsne = TSNE(n_components=2, metric="precomputed", init="random", random_state=42)
    tsne_coordinates = tsne.fit_transform(distance_df.values)
    
    # Perform K-Means clustering on the distance matrix
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_labels = kmeans.fit_predict(distance_df)

    # Scatter plot of t-SNE coordinates
    plt.figure(figsize=(12, 8))
    plt.scatter(tsne_coordinates[:, 0], tsne_coordinates[:, 1], c=kmeans_labels, cmap='viridis', s=100)

    # Annotate and highlight specific countries
    for i, country in enumerate(distance_df.index):
        if country in highlight_countries:
            plt.scatter(
                tsne_coordinates[i, 0],
                tsne_coordinates[i, 1],
                color='red',
                s=200,
                edgecolor='black',
            )
            plt.annotate(
                country,
                (tsne_coordinates[i, 0] + 0.1, tsne_coordinates[i, 1] + 0.1),
                fontsize=12,
                fontweight='bold',
                color='white',
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='black'),
            )
        else:
            plt.annotate(
                country,
                (tsne_coordinates[i, 0] + 0.05, tsne_coordinates[i, 1] + 0.05),
                fontsize=8,
                color='black',
            )

    plt.title(title)
    plt.xlabel('t-SNE Dimension 1')
    plt.ylabel('t-SNE Dimension 2')
    plt.tight_layout()
    plt.savefig(f'figures/{title}.png', format='png', dpi=PLOT_STYLE['dpi'])
    if show:
        plt.show()

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

def boxplot_with_highlight(distance_df, country, highlight_countries, title="", show=False):
    """
    Create a styled box plot of all distances for a specific country, highlighting specific distances.

    Args:
        distance_df (pd.DataFrame): A DataFrame containing the distance matrix.
        country (str): The country for which to plot distances.
        highlight_countries (list): List of countries to highlight in the box plot.
    """
    if country not in distance_df.index:
        print(f"Country '{country}' not found in the dataset.")
        return

    # Extract distances for the specified country
    distances = distance_df.loc[country].drop(country)  # Exclude the self-distance
    highlighted_values = {highlight: distances[highlight] for highlight in highlight_countries if highlight in distances.index}

    # Create the box plot
    fig, ax = plt.subplots(figsize=(8, 6))
    box = ax.boxplot(
        distances.values,
        vert=True,
        patch_artist=False,  # No filling
        boxprops=dict(color='black', linewidth=1.5),
        whiskerprops=dict(color='black', linewidth=1.5),
        capprops=dict(color='black', linewidth=1.5),
        medianprops=dict(color='black', linewidth=1.5),
        meanline=True,  # Show the average line
        meanprops=dict(color='black', linestyle='--', linewidth=1.5),
    )

    # Highlight specific points with a fine 'X'
    x_coords = [1] * len(highlighted_values)  # All points are in box position 1
    y_coords = list(highlighted_values.values())
    ax.scatter(x_coords, y_coords, color='black', marker='x', s=50, zorder=3, label="Highlighted Distances")

    # Add annotations for highlighted countries (outside the boxplot)
    for i, (country_name, y) in enumerate(highlighted_values.items()):
        ax.annotate(
            country_name,
            (1.1, y),  # Position text outside the boxplot
            fontsize=9,  # Smaller, fine text
            fontweight='regular',
            color='black',
            verticalalignment='center',
            horizontalalignment='left',
        )

    # Customize plot
    ax.set_title(f"Distances from {country}", fontsize=14, color='black')
    ax.set_ylabel("Distance", fontsize=12, color='black')
    ax.set_xticks([1])
    ax.set_xticklabels([country], fontsize=12, color='black')
    ax.tick_params(axis='y', colors='black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('none')  # Remove right spine
    ax.spines['top'].set_color('none')  # Remove top spine
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Save and show the plot
    plt.tight_layout()
    plt.savefig(f"figures/{title} - {country}_distance_boxplot_styled.png", format="png", dpi=300)
    if show:
        plt.show()
