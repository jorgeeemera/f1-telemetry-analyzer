# F1 Telemetry & Strategy Analyzer 🏎️📊

An end-to-end data pipeline designed for massive data extraction, mathematical transformation, and visualization of Formula 1 telemetry. 

This project simulates the workflow of a Motorsport Data Engineer, separating the backend processing logic in Python from the Business Intelligence frontend layer in Tableau.

## 🛠️ Architecture & Technologies
*   **Core Language:** Python 3.x
*   **Data Extraction:** Ergast API & `FastF1` library.
*   **Data Cleaning & Transformation:** `Pandas`.
*   **Mathematics & Time Series:** `NumPy` (Linear interpolation and spatial alignment for exact Delta Time calculation).
*   **Scientific Visualization:** `Matplotlib` & `Seaborn` (Track Dominance Maps and GridSpecs).
*   **Business Intelligence (Frontend):** Tableau (Interactive self-service dashboards).

## 🚀 Project Files

1.  `01_extract_telemetry.py`: Initial ETL script. Cache configuration, API ingestion, and tabular data structuring.
2.  `02_visualize_telemetry.py`: Static generation of speed trace comparisons using Matplotlib.
3.  `03_race_pace_degradation.py`: Race pace analysis, outlier filtering (e.g., Safety Cars, Pit Stops), and linear regression modeling to predict tire degradation.
4.  `04_delta_time.py`: The mathematical core. Resolving array length mismatches through spatial interpolation and generating an advanced track dominance dashboard.
5.  `05_etl_for_tableau.py`: Final data preparation. Exports a clean, geospatial relational model as a CSV, ready for ingestion into BI platforms.

## ⚙️ How to Run

1. Clone the repository:
```bash
   git clone [https://github.com/your-username/f1-telemetry-analyzer.git](https://github.com/your-username/f1-telemetry-analyzer.git)
```

2. Install the required dependencies:
```bash
    pip install -r requirements.txt
```

3. Run the scripts in order. Make sure you have write permissions in the root folder, as FastF1 will automatically generate a /cache directory to optimize API requests.

# 📈 Tableau Dashboard
The included .twbx (Tableau Packaged Workbook) file contains the interactive dashboard designed for the 2024 Monaco Grand Prix analysis. It allows users to dynamically filter telemetry data and spatial heatmaps by driver in real-time.