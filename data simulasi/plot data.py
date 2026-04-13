import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# 1. Data Waypoint Referensi (RPL)
rpl_lat = [-5.924208, -5.924051, -5.924222, -5.924041]
rpl_long = [105.992613, 105.992493, 105.992120, 105.991831]

# 2. Load Data dari CSV
try:
    # Load data Pseudoinverse biasa
    df_raw = pd.read_csv('pseudoinverse_log.csv')
    
    # Load data Pseudoinverse + Low Pass Filter
    df_lp = pd.read_csv('pseudoinverse+LP.csv')
    
    data_ready = True
except FileNotFoundError as e:
    print(f"Error: {e}")
    data_ready = False

# 3. Setup Figure
fig, ax = plt.subplots(figsize=(12, 8))

if data_ready:
    # Plot 1: RPL (Garis Biru Putus-putus)
    ax.plot(rpl_long, rpl_lat, 'b--', label='RPL (Reference)', alpha=0.5, linewidth=2)
    ax.scatter(rpl_long, rpl_lat, c='blue', s=40, zorder=5)

    # Plot 2: Pseudoinverse Biasa (Garis Merah tipis/transparan agar tidak menutupi yang lain)
    ax.plot(df_raw['long'], df_raw['lat'], 'r-', label='Pseudoinverse ()', alpha=0.4, linewidth=2)

    # Plot 3: Pseudoinverse + Low Pass Filter (Garis Hijau Tebal)
    # Ini adalah hasil yang seharusnya lebih smooth
    ax.plot(df_lp['long'], df_lp['lat'], 'g-', label='Pseudoinverse + Linear Programming', linewidth=2)

    # Penanda START & END
    ax.plot(rpl_long[0], rpl_lat[0], 'go', markersize=10, label='START')
    ax.plot(rpl_long[-1], rpl_lat[-1], 'ro', markersize=10, label='END')

# 4. Format Angka Desimal (Agar tidak jadi format scientific)
xfmt = ScalarFormatter(useOffset=False)
xfmt.set_scientific(False)
ax.xaxis.set_major_formatter(xfmt)
ax.yaxis.set_major_formatter(xfmt)

# 5. Label, Grid, dan Legend
plt.title('Vessel Trajectory')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='best')

# Zoom otomatis ke area data agar terlihat jelas
plt.tight_layout()
plt.show()