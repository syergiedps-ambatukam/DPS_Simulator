import numpy as np
from filterpy.kalman import KalmanFilter

# Dimensi state (x = [theta, omega]) dan measurement (y = theta)
dim_x = 2  
dim_z = 1  

kf = KalmanFilter(dim_x=dim_x, dim_z=dim_z)

# Model state-space (A, B, C)
kf.F = np.array([[0, 1], 
                 [-2, -3]])  # Matriks A (state transition)

kf.B = np.array([[0], 
                 [1]])  # Matriks B (kontrol)

kf.H = np.array([[1, 0]])  # Matriks C (observasi)

# Noise kovariansi
kf.Q = np.eye(dim_x) * 1e-4  # Noise proses
kf.R = np.array([[0.1]])  # Noise pengukuran
kf.P = np.eye(dim_x) * 1.0  # Kovariansi awal

# State awal
kf.x = np.array([[0],  # θ (posisi awal)
                 [0]])  # ω (kecepatan awal)

# Simulasi input kontrol (tegangan motor)
u = 1.0  # Tegangan konstan
measurements = [0.1, 0.2, 0.25, 0.4, 0.5]  # Contoh data sensor

for z in measurements:
    kf.predict(u= u)  # Prediksi dengan sinyal kendali
    kf.update(z)  # Update dengan data sensor
    print(z)
    print(f"Estimasi theta: {kf.x[0, 0]:.2f}, omega: {kf.x[1, 0]:.2f}")
