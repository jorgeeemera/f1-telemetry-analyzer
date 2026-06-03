import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = 'telemetria_monaco_q.csv'
df = pd.read_csv(data)

# 2. Styling
plt.style.use('dark_background')
sns.set_context("notebook", font_scale=1.1)

# Creating the figure
fig, ax = plt.subplots(figsize=(14, 6))

# 3. Split data by driver
lec_data = df[df['Driver'] == 'LEC']
pia_data = df[df['Driver'] == 'PIA']

# 4. Plot the drivers' lines
ax.plot(lec_data['Distance'], lec_data['Speed'], color='#DC0000', label='LEC (Ferrari)', linewidth=2)
ax.plot(pia_data['Distance'], pia_data['Speed'], color='#FF8700', label='PIA (McLaren)', linewidth=2, alpha=0.8)

# 5. Customize the graphic
ax.set_title("Telemetry comparison: C. Leclerc vs O. Piastri\nMónaco 2024 - Q3 (Fastest Lap)", 
             fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("Distance (m)", fontsize=12)
ax.set_ylabel("Speed (km/h)", fontsize=12)
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
ax.legend(loc='lower right', frameon=True, facecolor='black', edgecolor='white')

# 6. Saving the file
output_file = 'speed_comparison_monaco.png'
plt.tight_layout()
plt.savefig(output_file, dpi=300)
print(f"Graphic saved as {output_file}")

plt.show()