import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
try:
    df_raw = pd.read_csv('pseudoinverse_log.csv')
    df_lp = pd.read_csv('pseudoinverse+LP.csv')
    
    # 2. Setup Figure: 1 Halaman, 2 Baris (Subplots)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
    fig.suptitle('method 1 vs method 2', fontsize=16, fontweight='bold')

    # --- GRAFIK 1: RAW PSEUDOINVERSE (ATAS) ---
    # Fx
    ax1.plot(df_raw.index, df_raw['fx'], 'r--', label='Target Fx', alpha=0.5)
    ax1.plot(df_raw.index, df_raw['fx_actual'], 'r-', label='Actual Fx', linewidth=1.2)
    # Fy
    ax1.plot(df_raw.index, df_raw['fy'], 'g--', label='Target Fy', alpha=0.5)
    ax1.plot(df_raw.index, df_raw['fy_actual'], 'g-', label='Actual Fy', linewidth=1.2)
    # Mz
    ax1.plot(df_raw.index, df_raw['mz'], 'b--', label='Target Mz', alpha=0.5)
    ax1.plot(df_raw.index, df_raw['mz_actual'], 'b-', label='Actual Mz', linewidth=1.2)

    ax1.set_title('Grafik 1: Pseudoinverse', fontsize=12)
    ax1.set_ylabel('Value (N)')
    ax1.legend(loc='upper right', ncol=3, fontsize='8')
    ax1.grid(True, linestyle=':', alpha=0.6)

    # --- GRAFIK 2: PSEUDOINVERSE + LP (BAWAH) ---
    # Fx
    ax2.plot(df_lp.index, df_lp['fx'], 'r--', label='Target Fx', alpha=0.5)
    ax2.plot(df_lp.index, df_lp['fx_actual'], 'r-', label='Actual Fx', linewidth=1.2)
    # Fy
    ax2.plot(df_lp.index, df_lp['fy'], 'g--', label='Target Fy', alpha=0.5)
    ax2.plot(df_lp.index, df_lp['fy_actual'], 'g-', label='Actual Fy', linewidth=1.2)
    # Mz
    ax2.plot(df_lp.index, df_lp['mz'], 'b--', label='Target Mz', alpha=0.5)
    ax2.plot(df_lp.index, df_lp['mz_actual'], 'b-', label='Actual Mz', linewidth=1.2)

    ax2.set_title('Grafik 2: Pseudoinverse + Linear Programming', fontsize=12)
    ax2.set_ylabel('Value (N)')
    ax2.set_xlabel('Time Step')
    ax2.legend(loc='upper right', ncol=3, fontsize='8')
    ax2.grid(True, linestyle=':', alpha=0.6)

    # 3. Final Layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

except FileNotFoundError as e:
    print(f"Error: Salah satu file tidak ditemukan. Detail: {e}")