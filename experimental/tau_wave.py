import numpy as np
import matplotlib.pyplot as plt

# Parameter Gelombang
H = 2.0  # Tinggi gelombang (m)
L = 50.0  # Panjang gelombang (m)
T = 8.0  # Periode gelombang (s)
theta = 45  # Arah gelombang (derajat, relatif terhadap sumbu x)
rho = 1025  # Densitas air laut (kg/m^3)
g = 9.81  # Gravitasi (m/s^2)

# Parameter Struktur
A_x = 10.0  # Luas proyeksi struktur di arah x (m^2)
A_y = 8.0  # Luas proyeksi struktur di arah y (m^2)
C_x = 1.0  # Koefisien gaya di arah x
C_y = 1.0  # Koefisien gaya di arah y
r_N = 5.0  # Jarak dari pusat massa ke titik aplikasi gaya (m)

# Perhitungan dasar
omega = 2 * np.pi / T  # Frekuensi sudut gelombang (rad/s)
k = 2 * np.pi / L  # Bilangan gelombang (rad/m)

# Fungsi kecepatan partikel gelombang
def wave_velocity(H, omega, k, x, z, t):
    return (H * omega / 2) * np.cosh(k * (z + H)) / np.sinh(k * H) * np.sin(omega * t - k * x)

# Simulasi waktu
time = np.linspace(0, T, 100)  # 100 langkah waktu dalam 1 periode
tau_x = []
tau_y = []
tau_N = []

# Simulasi gaya
for t in time:
    # Kecepatan partikel di x dan y
    u_x = wave_velocity(H, omega, k, 0, 0, t) * np.cos(np.radians(theta))
    u_y = wave_velocity(H, omega, k, 0, 0, t) * np.sin(np.radians(theta))
    
    # Gaya gelombang di x dan y
    Fx = rho * C_x * A_x * u_x**2
    Fy = rho * C_y * A_y * u_y**2
    
    # Momen gelombang
    Tn = r_N * Fy  # Diasumsikan momen dihasilkan dari gaya di arah y
    
    tau_x.append(Fx)
    tau_y.append(Fy)
    tau_N.append(Tn)

# Plot hasil simulasi
plt.figure(figsize=(10, 6))
plt.plot(time, tau_x, label=r'$\tau_x$ (Gaya arah x)')
plt.plot(time, tau_y, label=r'$\tau_y$ (Gaya arah y)')
plt.plot(time, tau_N, label=r'$\tau_N$ (Momen)')
plt.xlabel('Waktu (s)')
plt.ylabel('Gaya/Momen (N atau Nm)')
plt.title('Simulasi $\tau_x$, $\tau_y$, dan $\tau_N$ dari Gelombang')
plt.legend()
plt.grid(True)
plt.show()
