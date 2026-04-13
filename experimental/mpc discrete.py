import numpy as np
from scipy.optimize import minimize

# Fungsi model dinamika suhu
def model(T_k, u_k, T_ext=20):
    return T_k + 0.5 * u_k + 0.2 * (T_ext - T_k)

# Fungsi biaya (cost function) untuk MPC
def cost_function(u, T_0, T_ref, N=3, Q=10, R=1):
    """
    u: Array input kontrol untuk horizon prediksi (misalnya u_1, u_2, ..., u_N)
    T_0: Suhu awal
    T_ref: Suhu yang diinginkan (referensi)
    N: Horizon prediksi
    Q: Bobot penalti kesalahan suhu
    R: Bobot penalti input kontrol
    """
    T_k = T_0
    J = 0
    for i in range(N):
        # Prediksi suhu pada langkah ke-i
        T_k = model(T_k, u[i])
        
        # Hitung kesalahan suhu dan penalti input kontrol
        error = T_k - T_ref
        J += Q * error**2 + R * u[i]**2
        
        # Print prediksi suhu pada setiap langkah
        print(f"Langkah {i+1}: Prediksi Suhu = {T_k:.2f}°C, Kontrol = {u[i]:.2f}")
    return J

# Fungsi untuk menyelesaikan optimisasi MPC
def mpc(T_0, T_ref, N=3, Q=10, R=1, u_min=0, u_max=100):
    # Inisialisasi kontrol pertama (misal semua kontrol 0.5)
    u_init = np.ones(N) * 0.5
    
    # Kendala pada kontrol (0 <= u_k <= 1)
    bounds = [(u_min, u_max) for _ in range(N)]
    
    # Optimisasi dengan scipy minimize
    result = minimize(cost_function, u_init, args=(T_0, T_ref, N, Q, R),
                      bounds=bounds, method='SLSQP')
    
    # Mengembalikan input kontrol optimal dan nilai fungsi biaya
    return result.x, result.fun

# Parameter sistem
T_0 = 20  # Suhu awal ruangan
T_ref = 22  # Suhu yang diinginkan
N = 100  # Horizon prediksi
Q = 10  # Bobot penalti kesalahan suhu
R = 1   # Bobot penalti input kontrol

# Menyelesaikan optimisasi MPC
u_opt, J_opt = mpc(T_0, T_ref, N, Q, R)

# Tampilkan hasil optimisasi dan prediksi
print("\nOptimisasi selesai:")
print("Kontrol Optimal:", u_opt)
print("Nilai Fungsi Biaya Optimal:", J_opt)

# Prediksi suhu setelah kontrol optimal diterapkan
T_pred = T_0
print("\nPrediksi Suhu Akhir setelah Kontrol Optimal:")
for i in range(N):
    T_pred = model(T_pred, u_opt[i])
    print(f"Langkah {i+1}: Suhu = {T_pred:.2f}°C")
    print("--------")
