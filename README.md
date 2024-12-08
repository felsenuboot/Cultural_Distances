<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️-->
[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#cultural-distances-project-overview)

# ➤ Cultural Distances: Project Overview

This repository contains Python scripts and associated files for processing, analyzing, and visualizing cultural data. The project uses various Python libraries for data manipulation and machine learning.

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#how-to-use)

## ➤ How to Use

> [!NOTE]  
> Make sure python is installed. 

1. **Clone the Repository**

   ```bash
   git clone https://github.com/felsenuboot/Cultural_Distances.git
   cd Cultural_Distances
   ```

2. **Install Dependencies**
   Make sure you have Python installed (version >= 3.8). Then, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scripts**
   ```bash
   python main.py -t -s
   ```


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#files-in-this-repository)

## ➤ Files in This Repository

### 1. `convert_data.py`

This script contains functions to process raw data, transform it into a usable format, and prepare it for analysis or visualization. The script likely handles tasks such as:

- Data cleaning
- Format conversions
- Data validation

### 2. `main.py`

This script serves as the entry point for the project. 

- Running analysis or model training pipelines
- Generating visualizations or reports based on processed data

### 3. `requirements.txt`

This file lists all the Python dependencies required to run the project. Use it to install the necessary libraries with the following command:

```bash
pip install -r requirements.txt
```


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#dependencies)

## ➤ Dependencies

The project relies on the following Python packages:

- Data manipulation and analysis: `numpy`, `pandas`, `openpyxl`
- Visualization: `matplotlib`, `seaborn`
- Machine Learning: `scikit-learn`
- Others: `networkx`, `joblib`, `scipy`

For a complete list, refer to the `requirements.txt` file.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#notes)

## ➤ Notes

- Ensure your input data meets the expected format required by `convert_data.py`. Check the script for details on input and output specifications.
- If any issues arise, ensure all dependencies are installed and compatible with your Python version.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#contributing)

## ➤ Contributing

Feel free to contribute by submitting pull requests. Make sure to:

- Document any new functions or features.
- Test your changes thoroughly.
