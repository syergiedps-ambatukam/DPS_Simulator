import numpy as np
from scipy.optimize import minimize
import math
steering1 = 45
steering2 = -45
steering3 = 135
steering4 = -135

ly1 = 0.5
lx1 = 0.5

ly2 = -0.5
lx2 = 0.5

ly3 = -0.5
lx3 = -0.5

ly4 = 0.5
lx4 = -0.5


# 1. Definisi Matriks (Sama seperti kode kamu)
T_nonlinear = np.array([
    [np.cos(np.deg2rad(steering1)), np.cos(np.deg2rad(steering2)), np.cos(np.deg2rad(steering3)), np.cos(np.deg2rad(steering4))],         # Fx
    [np.sin(np.deg2rad(steering1)), np.sin(np.deg2rad(steering2)), np.sin(np.deg2rad(steering3)), np.sin(np.deg2rad(steering4))],         # Fy
    # Ganti baris Mz di T_nonlinear menjadi:
    [
        ((lx1 * np.sin(np.deg2rad(steering1))) - (ly1 * np.cos(np.deg2rad(steering1)))),
        ((lx2 * np.sin(np.deg2rad(steering2))) - (ly2 * np.cos(np.deg2rad(steering2)))),
        ((lx3 * np.sin(np.deg2rad(steering3))) - (ly3 * np.cos(np.deg2rad(steering3)))),
        ((lx4 * np.sin(np.deg2rad(steering4))) - (ly4 * np.cos(np.deg2rad(steering4))))
    ]   # Mz
])
b_eq = np.array([2, 1, 1])


print(T_nonlinear)
# 2. Fungsi Objektif: Meminimalkan error (Ax - b)^2
def objective(x):
    error = np.dot(T_nonlinear, x) - b_eq
    return np.sum(error**2) # Least squares error

# 3. Batasan (Bounds): 0 <= Fi <= 5
bounds = [(0, 5) for _ in range(4)]

print(bounds)
# 4. Tebakan awal (Initial guess)
x0 = np.array([2.5, 2.5, 2.5, 2.5])

# 5. Jalankan optimasi
res = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

if res.success:
    F = res.x
    print("Solusi Terdekat yang Memungkinkan:")
    print(f"F1 = {F[0]:.3f}, F2 = {F[1]:.3f}, F3 = {F[2]:.3f}, F4 = {F[3]:.3f}")
    
    # Cek seberapa dekat hasilnya ke target
    actual_b = np.dot(T_nonlinear, F)
    print("\nTarget vs Hasil Nyata:")
    print(f"Fx: Target {b_eq[0]} -> Hasil {actual_b[0]:.3f}")
    print(f"Fy: Target {b_eq[1]} -> Hasil {actual_b[1]:.3f}")
    print(f"Mz: Target {b_eq[2]} -> Hasil {actual_b[2]:.3f}")
else:
    print("Gagal mencari solusi terdekat.")
    
    
#Recheck dengan T Linear
    
#F real + noise
fx1_real = F[0] * math.cos(np.deg2rad(steering1))
fx2_real = F[1] * math.cos(np.deg2rad(steering2))
fx3_real = F[2] * math.cos(np.deg2rad(steering3))
fx4_real = F[3] * math.cos(np.deg2rad(steering4))

fy1_real = F[0] * math.sin(np.deg2rad(steering1))
fy2_real = F[1] * math.sin(np.deg2rad(steering2))
fy3_real = F[2] * math.sin(np.deg2rad(steering3))
fy4_real = F[3] * math.sin(np.deg2rad(steering4))

f_real = np.array([
                fx1_real, fy1_real,
                fx2_real, fy2_real,
                fx3_real, fy3_real,
                fx4_real, fy4_real
            ]).reshape(8, 1)
print(f_real)
T = np.array([[1, 0, 1, 0, 1, 0, 1, 0],   # Menambah kolom untuk F_x4
              [0, 1, 0, 1, 0, 1, 0, 1],   # Menambah kolom untuk F_y4
              [-ly1, lx1, -ly2, lx2, -ly3, lx3, -ly4, lx4]])  # Menyesuaikan gaya kontrol

u_real = T @ f_real   # ← FINAL & BENAR
print("u_linear",u_real)           