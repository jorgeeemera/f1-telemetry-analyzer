import fastf1
import pandas as pd

# 1. Configure session
fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2024, 'Monaco', 'Q')
session.load()

# 2. Get the 5 fastest drivers of the session
results = session.results.head(5)
top_5_drivers = results['Abbreviation'].tolist()
print(f"Extracting data for: {top_5_drivers}")

# 3. ETL Loop: Extract and stack telemetry for all
telemetry_list = []

for driver in top_5_drivers:
    lap = session.laps.pick_driver(driver).pick_fastest()
    tel = lap.get_telemetry()
    
    # We select only the key columns for Tableau
    # X and Y are crucial for drawing the map in Tableau
    clean_tel = tel[['Distance', 'Speed', 'nGear', 'X', 'Y']].copy()
    clean_tel['Driver'] = driver
    
    telemetry_list.append(clean_tel)

# 4. Consolidate into a single DataFrame
df_tableau = pd.concat(telemetry_list, ignore_index=True)

# 5. Export to CSV
output_file = 'f1_telemetry_for_tableau.csv'
df_tableau.to_csv(output_file, index=False)
print(f"ETL complete! Dataset ready for Tableau saved as {output_file}")