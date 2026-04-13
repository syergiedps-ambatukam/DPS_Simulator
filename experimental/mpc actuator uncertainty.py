import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# ===== Parameter Sistem =====
A = np.array([[1, 0.1], [0, 1]])  # Matriks state (2, 2)
B = np.array([[0], [0.1]])         # Matriks kontrol (2, 1)
C = np.array([[1, 0]])             # Matriks output (1, 2)
Q = np.eye(1)                      # Bobot error (1, 1)
R = 0.1 * np.eye(1)                # Bobot kontrol (1, 1)
P = np.eye(2)                      # Bobot terminal state (2, 2)
delta_u_penalty = 0.01 * np.eye(1) # Bobot perubahan kontrol (1, 1)
u_min = -1                         # Batas bawah kontrol
u_max = 1                          # Batas atas kontrol
N = 10                             # Horizon prediksi
x0 = np.array([[0], [0]])          # State awal (2, 1)
y_ref = np.array([[1]])            # Referensi output (1, 1)

# ===== Parameter Aktuator =====
tau = 0.2  # Konstanta waktu aktuator (sistem orde pertama)
u_actual_prev = 0  # Respons aktual sebelumnya

# ===== Simulasi =====
sim_steps = 50  # Jumlah langkah simulasi
x_history = []  # Untuk menyimpan history state
u_mpc_history = []  # Untuk menyimpan history sinyal kendali MPC
u_actual_history = []  # Untuk menyimpan history respons aktual
y_history = []  # Untuk menyimpan history output

# Loop simulasi
for step in range(sim_steps):
    # ===== MPC =====
    # Variabel Optimisasi
    x = cp.Variable((A.shape[0], N + 1))  # State variables (2, N+1)
    u = cp.Variable((B.shape[1], N))      # Control inputs (1, N)

    # Fungsi Biaya dan Kendala
    cost = 0
    constraints = []

    for k in range(N):
        cost += cp.quad_form(C @ x[:, k] - y_ref.flatten(), Q)  # Penalti error
        cost += cp.quad_form(u[:, k], R)  # Penalti kontrol
        if k > 0:
            cost += cp.quad_form(u[:, k] - u[:, k - 1], delta_u_penalty)  # Penalti perubahan kontrol
        constraints += [x[:, k + 1] == A @ x[:, k] + B @ u[:, k]]  # Persamaan state
        constraints += [u_min <= u[:, k], u[:, k] <= u_max]  # Kendala kontrol

    # Status awal
    constraints += [x[:, 0] == x0.flatten()]

    # Problem MPC
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve()

    # Ambil kontrol optimal
    if problem.status != 'optimal':
        print(f"Solver failed at step {step}. Status: {problem.status}")
        break

    u_mpc = u.value[:, 0]  # Sinyal kendali dari MPC

    # ===== Model Aktuator =====
    # Simulasikan respons aktual aktuator (sistem orde pertama)
    u_actual = u_actual_prev + (u_mpc - u_actual_prev) / tau
    u_actual = np.clip(u_actual, u_min, u_max)  # Batasi respons aktual
    u_actual_prev = u_actual  # Update respons sebelumnya

    # ===== Update Sistem =====
    x0 = A @ x0 + B @ u_actual  # Update state sistem dengan respons aktual
    y = C @ x0  # Output sistem

    # Simpan history
    x_history.append(x0.flatten())
    u_mpc_history.append(u_mpc.flatten())
    u_actual_history.append(u_actual.flatten())
    y_history.append(y.flatten())

# ===== Plot Hasil =====
plt.figure(figsize=(12, 8))

# Plot State
plt.subplot(3, 1, 1)
plt.plot(x_history, label=['x1', 'x2'])
plt.title('State Sistem')
plt.xlabel('Langkah Waktu')
plt.ylabel('State')
plt.legend()

# Plot Sinyal Kendali
plt.subplot(3, 1, 2)
plt.plot(u_mpc_history, label='u_MPC')
plt.plot(u_actual_history, label='u_actual', linestyle='--')
plt.title('Sinyal Kendali MPC vs Respons Aktual Aktuator')
plt.xlabel('Langkah Waktu')
plt.ylabel('Kontrol')
plt.legend()

# Plot Output
plt.subplot(3, 1, 3)
plt.plot(y_history, label='Output (y)')
plt.axhline(y=y_ref, color='r', linestyle='--', label='Referensi (y_ref)')
plt.title('Output Sistem')
plt.xlabel('Langkah Waktu')
plt.ylabel('Output')
plt.legend()

plt.tight_layout()
plt.show()