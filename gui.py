import json
import os
import pandas as pd
from scipy.spatial.distance import pdist, squareform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from sklearn.manifold import MDS, TSNE
from sklearn.cluster import KMeans
import networkx as nx
import numpy as np


def calculate_scaled_euclidean_distances(data, score_key="scores"):
    countries = [item["name"] for item in data]
    scores = [item[score_key] for item in data]
    scores_df = pd.DataFrame(scores, index=countries).replace(-1, pd.NA).dropna(axis=1, how="any")
    variances = scores_df.var().values
    distances = pdist(scores_df, metric="seuclidean", V=variances)
    distance_matrix = squareform(distances)
    return pd.DataFrame(distance_matrix, index=countries, columns=countries)


def visualize_country_network(distance_df, title="Network Graph of Country Distances"):
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

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="black")
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7, edge_color="black")
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="white")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.axis("off")
    plt.title(title)
    plt.show()


def export_distances_to_csv(distance_df, title):
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        distance_df.to_csv(filename)
        messagebox.showinfo("Export Success", f"Distances exported to {filename}")


def find_max_min_distances(distance_df):
    max_distance = distance_df.where(~np.eye(distance_df.shape[0], dtype=bool)).max().max()
    min_distance = distance_df.where(~np.eye(distance_df.shape[0], dtype=bool)).min().min()
    max_location = distance_df.where(distance_df == max_distance).stack().idxmax()
    min_location = distance_df.where(distance_df == min_distance).stack().idxmin()

    return max_distance, max_location, min_distance, min_location


def load_dataset():
    filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if filepath:
        with open(filepath, 'r') as f:
            return json.load(f), os.path.basename(filepath)
    return None, None


class CulturalDimensionsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cultural Dimensions GUI")
        self.master.geometry("600x400")

        self.data = None
        self.distance_df = None
        self.dataset_name = None

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.master, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Cultural Dimensions GUI", font=("Arial", 18)).pack(pady=10)

        ttk.Button(frame, text="Load Dataset", command=self.load_dataset).pack(pady=5)
        ttk.Button(frame, text="Visualize Network", command=self.visualize_network).pack(pady=5)
        ttk.Button(frame, text="Export Distances to CSV", command=self.export_csv).pack(pady=5)
        ttk.Button(frame, text="Find Max/Min Distances", command=self.show_max_min).pack(pady=5)

    def load_dataset(self):
        self.data, self.dataset_name = load_dataset()
        if self.data:
            self.distance_df = calculate_scaled_euclidean_distances(self.data)
            messagebox.showinfo("Dataset Loaded", f"Loaded dataset: {self.dataset_name}")

    def visualize_network(self):
        if self.distance_df is not None:
            visualize_country_network(self.distance_df, title=f"{self.dataset_name} Network Graph")
        else:
            messagebox.showerror("Error", "Please load a dataset first.")

    def export_csv(self):
        if self.distance_df is not None:
            export_distances_to_csv(self.distance_df, self.dataset_name)
        else:
            messagebox.showerror("Error", "Please load a dataset first.")

    def show_max_min(self):
        if self.distance_df is not None:
            max_dist, max_loc, min_dist, min_loc = find_max_min_distances(self.distance_df)
            messagebox.showinfo(
                "Max/Min Distances",
                f"Maximum Distance: {max_dist:.2f} (Between {max_loc[0]} and {max_loc[1]})\n"
                f"Minimum Distance: {min_dist:.2f} (Between {min_loc[0]} and {min_loc[1]})"
            )
        else:
            messagebox.showerror("Error", "Please load a dataset first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CulturalDimensionsApp(root)
    root.mainloop()