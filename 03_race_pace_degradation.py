import fastf1
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Enable cache and load the Monaco 2024 Race ('R' for Race)
fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2024, 'Monaco', 'R')
session.load()

# 2. Select the drivers to compare
drivers = ['LEC', 'PIA']
laps = session.laps.pick_drivers(drivers)

# 3. CRITICAL TRANSFORMATION (Data Cleaning)
# Exclude pit in/out laps, Safety Car laps, or red flag laps
clean_laps = laps.pick_accurate()

# Lap times are in 'timedelta' format. 
# To plot them, we need to transform them to seconds (decimal number).
clean_laps = clean_laps.assign(LapTime_s=clean_laps['LapTime'].dt.total_seconds())

# 4. Advanced Visualization (F1 Style)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 6))

# 5. Scatter Plot of lap times
sns.scatterplot(data=clean_laps, x='LapNumber', y='LapTime_s', 
                hue='Driver', palette={'LEC': '#DC0000', 'PIA': '#FF8700'}, 
                s=60, alpha=0.8, ax=ax)

# 6. Add Trend Lines (Linear regression to see degradation)
sns.regplot(data=clean_laps[clean_laps['Driver'] == 'LEC'], 
            x='LapNumber', y='LapTime_s', scatter=False, color='#DC0000', ax=ax, label='LEC Trend')
sns.regplot(data=clean_laps[clean_laps['Driver'] == 'PIA'], 
            x='LapNumber', y='LapTime_s', scatter=False, color='#FF8700', ax=ax, label='PIA Trend')

# 7. Customize the plot
ax.set_title("Race Pace and Degradation Analysis\nMonaco 2024 - Leclerc vs Piastri", 
             fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("Lap Number", fontsize=12)
ax.set_ylabel("Lap Time (Seconds)", fontsize=12)

# Improve Y-axis readability
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

# 8. Save and show
output_file = 'race_pace_monaco.png'
plt.tight_layout()
plt.savefig(output_file, dpi=300)
print(f"Race pace plot saved as {output_file}")

plt.show()