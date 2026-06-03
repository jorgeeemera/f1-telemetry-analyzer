import fastf1
import pandas as pd

# 1. Enable cache
fastf1.Cache.enable_cache('cache')

# 2. Load a specific session (Monaco 2024, Qualifying)
session = fastf1.get_session(2024, 'Monaco', 'Q')
session.load()

# 3. Extract the fastest laps of two drivers to compare
driver_1 = 'LEC'
driver_2 = 'PIA'

lap_d1 = session.laps.pick_driver(driver_1).pick_fastest()
lap_d2 = session.laps.pick_driver(driver_2).pick_fastest()

# 4. Get the telemetry for that exact lap
telemetry_d1 = lap_d1.get_telemetry()
telemetry_d2 = lap_d2.get_telemetry()

print(f"--- Telemetry for {driver_1} ---")
print(telemetry_d1[['Distance', 'Speed', 'nGear', 'Throttle', 'Brake']].head())

# 5. Transformation: Add a column to identify the driver
telemetry_d1['Driver'] = driver_1
telemetry_d2['Driver'] = driver_2

# 6. Join the data from both drivers into a single table
total_telemetry = pd.concat([telemetry_d1, telemetry_d2])

# 7. Load: Export to a clean CSV file
file_name = 'telemetry_monaco_q.csv'
total_telemetry.to_csv(file_name, index=False)
print(f"\nData successfully exported to {file_name}!")