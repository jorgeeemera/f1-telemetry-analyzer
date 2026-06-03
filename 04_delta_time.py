import fastf1
from fastf1 import utils
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import seaborn as sns

# 1. Enable cache and load the session
fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2024, 'Monaco', 'Q')
session.load()
circuit_info = session.get_circuit_info()

# 2. Select drivers and calculate Delta Time
driver_1 = 'LEC'
driver_2 = 'PIA'
color_d1 = '#DC0000' # Ferrari Red
color_d2 = '#FF8700' # McLaren Orange

lap_d1 = session.laps.pick_driver(driver_1).pick_fastest()
lap_d2 = session.laps.pick_driver(driver_2).pick_fastest()

# Generate the delta and aligned tables (ref_tel and compare_tel)
delta_time, ref_tel, compare_tel = utils.delta_time(lap_d1, lap_d2)

# Get the original telemetry to extract GPS data
tel_d1 = lap_d1.get_telemetry()

# --- THE MASTER SOLUTION: Spatial Interpolation ---
# We interpolate X and Y to match the length of ref_tel exactly
x = np.interp(ref_tel['Distance'], tel_d1['Distance'], tel_d1['X'])
y = np.interp(ref_tel['Distance'], tel_d1['Distance'], tel_d1['Y'])

# 3. PREPARE THE MAP: Coordinates and Colors (LineCollection)
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Assign color based on delta time
dominance_colors = [color_d1 if d < 0 else color_d2 for d in delta_time[:-1]]

# 4. DASHBOARD DESIGN (GridSpec)
plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 8))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.5]) 
fig.suptitle(f"Advanced Dominance and Telemetry Analysis\n{driver_1} vs {driver_2} - Monaco 2024 (Q3)", 
             fontsize=18, fontweight='bold')

# --- LEFT PANEL: Track Dominance Map ---
ax_map = fig.add_subplot(gs[:, 0])
lc = LineCollection(segments, colors=dominance_colors, linewidths=5)
ax_map.add_collection(lc)

for _, corner in circuit_info.corners.iterrows():
    ax_map.text(corner['X'], corner['Y'], str(corner['Number']), 
                color='white', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='circle', facecolor='black', alpha=0.6, edgecolor='gray'))

ax_map.set_title("Track Dominance (Who was faster each meter)", fontsize=12)
ax_map.axis('equal') 
ax_map.axis('off')   

# --- TOP RIGHT PANEL: Delta Time ---
# We use ref_tel so that everything matches perfectly
ax_delta = fig.add_subplot(gs[0, 1])
ax_delta.plot(ref_tel['Distance'], delta_time, color='white', linewidth=2)
ax_delta.axhline(0, color='gray', linestyle='--', alpha=0.6)
ax_delta.set_ylabel("Delta (s)", fontsize=12)
ax_delta.fill_between(ref_tel['Distance'], delta_time, 0, where=delta_time < 0, color=color_d1, alpha=0.6)
ax_delta.fill_between(ref_tel['Distance'], delta_time, 0, where=delta_time > 0, color=color_d2, alpha=0.6)
ax_delta.set_title("Delta Time (Accumulated time difference)", fontsize=12)

# --- BOTTOM RIGHT PANEL: Speed ---
ax_speed = fig.add_subplot(gs[1, 1], sharex=ax_delta) 
ax_speed.plot(ref_tel['Distance'], ref_tel['Speed'], color=color_d1, label=f'{driver_1} (Ferrari)')
ax_speed.plot(compare_tel['Distance'], compare_tel['Speed'], color=color_d2, label=f'{driver_2} (McLaren)', alpha=0.8)
ax_speed.set_xlabel("Distance (meters)", fontsize=12)
ax_speed.set_ylabel("Speed (km/h)", fontsize=12)
ax_speed.legend(loc='lower right')

for _, corner in circuit_info.corners.iterrows():
    ax_delta.axvline(corner['Distance'], color='grey', linestyle=':', alpha=0.3)
    ax_speed.axvline(corner['Distance'], color='grey', linestyle=':', alpha=0.3)

for ax in [ax_delta, ax_speed]:
    ax.set_xlim(0, max(ref_tel['Distance']))
    ax.grid(False)

plt.tight_layout()

# 5. Save the image
output_file = 'dashboard_dominance_monaco.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Engineer dashboard complete! Saved as {output_file}")

plt.show()