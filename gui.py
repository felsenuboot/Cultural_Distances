import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
import pandas as pd
import json

class CulturalDimensionsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cultural Dimensions Application")
        self.root.geometry("800x600")
        
        # Load datasets
        with open("data/hofstede_data.json", "r") as f:
            self.hofstede_data = json.load(f)
        with open("data/culture_map_data.json", "r") as f:
            self.culture_map_data = json.load(f)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Dataset selection
        self.dataset_var = tk.StringVar(value="Hofstede")
        dataset_label = ttk.Label(self.root, text="Select Dataset:")
        dataset_label.pack(pady=5)
        dataset_dropdown = ttk.Combobox(
            self.root, textvariable=self.dataset_var, values=["Hofstede", "Culture Map"]
        )
        dataset_dropdown.pack(pady=5)
        
        # Country selection
        self.country_var = tk.StringVar()
        country_label = ttk.Label(self.root, text="Select Country:")
        country_label.pack(pady=5)
        self.country_dropdown = ttk.Combobox(self.root, textvariable=self.country_var)
        self.country_dropdown.pack(pady=5)
        
        # Highlighted countries
        self.highlight_entry = tk.Entry(self.root)
        highlight_label = ttk.Label(self.root, text="Highlight Countries (comma-separated):")
        highlight_label.pack(pady=5)
        self.highlight_entry.pack(pady=5)
        
        # Action buttons
        self.create_buttons()
        
    def create_buttons(self):
        buttons = [
            ("Extract Distance", self.extract_distance),
            ("Visualize Network", self.visualize_network),
            ("Run K-Means Clustering", self.run_kmeans),
            ("Export Distances to CSV", self.export_distances),
            ("Find Max/Min Distances", self.find_max_min_distances),
            ("Boxplot with Highlight", self.create_boxplot),
        ]
        for text, command in buttons:
            ttk.Button(self.root, text=text, command=command).pack(pady=5)
    
    def get_selected_data(self):
        return self.hofstede_data if self.dataset_var.get() == "Hofstede" else self.culture_map_data
    
    def extract_distance(self):
        data = self.get_selected_data()
        distance_df = calculate_scaled_euclidean_distances(data)
        country1 = self.country_var.get()
        highlights = [c.strip() for c in self.highlight_entry.get().split(",")]
        if country1 in distance_df.index:
            distances = distance_df.loc[country1, highlights]
            messagebox.showinfo("Distances", f"Distances: {distances.to_dict()}")
        else:
            messagebox.showerror("Error", "Country not found in dataset.")
    
    def visualize_network(self):
        data = self.get_selected_data()
        distance_df = calculate_scaled_euclidean_distances(data)
        visualize_country_network(distance_df, title="Network Graph", show=True)
        messagebox.showinfo("Info", "Network visualization created.")
    
    def run_kmeans(self):
        data = self.get_selected_data()
        distance_df = calculate_scaled_euclidean_distances(data)
        plot_kmeans_with_highlight_MDS(distance_df, title="K-Means MDS", show=True)
        plot_kmeans_with_highlight_t_SNE(distance_df, title="K-Means t-SNE", show=True)
        messagebox.showinfo("Info", "K-Means clustering visualizations created.")
    
    def export_distances(self):
        data = self.get_selected_data()
        distance_df = calculate_scaled_euclidean_distances(data)
        export_distances_to_csv(distance_df, title=self.dataset_var.get())
        messagebox.showinfo("Info", "Distances exported to CSV.")
    
    def find_max_min_distances(self):
        data = self.get_selected_data()
        distance_df = calculate_scaled_euclidean_distances(data)
        max_distance = distance_df.max().max()
        min_distance = distance_df.min().min()
        messagebox.showinfo("Distances", f"Max Distance: {max_distance}, Min Distance: {min_distance}")
    
    def create_boxplot(self):
        data = self.get_selected_data()
        distance_df = calculate_scaled_euclidean_distances(data)
        country = self.country_var.get()
        highlights = [c.strip() for c in self.highlight_entry.get().split(",")]
        boxplot_with_highlight(distance_df, country, highlights, title="Boxplot", show=True)
        messagebox.showinfo("Info", "Boxplot created.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CulturalDimensionsApp(root)
    root.mainloop()