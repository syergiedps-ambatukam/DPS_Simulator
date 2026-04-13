import cvxpy as cp
import numpy as np

# Parameter sistem
np.random.seed(42)  # Untuk replikasi
A = np.array([[1.0, 1.0], [0, 1.0]])  # Matriks state transition
B = np.array([[0.5], [1.0]])  # Matriks kontrol
C = np.array([[1.0, 0.0]])  # Matriks output

# Parameter MPC
N = 10  # Horizon prediksi
Q = np.eye(1) * 10  # Penalti kesalahan output
R = np.eye(1) * 1  # Penalti kontrol

delta_u_penalty = np.eye(1) * 0.1  # Penalti perubahan kontrol
u_min = np.array([-1.0])  # Batas bawah kontrol
u_max = np.array([1.0])   # Batas atas kontrol

y_ref = np.array([[5.0]])  # Setpoint output

# Variabel optimisasi
x = cp.Variable((A.shape[0], N + 1))  # State variables
u = cp.Variable((B.shape[1], N))  # Control inputs
w = cp.Variable((A.shape[0], N))  # Disturbance

# Fungsi biaya dan kendala
cost = 0
constraints = []

for k in range(N):
    cost += cp.quad_form(C @ x[:, k] - y_ref.flatten(), Q)  # Penalti error
    cost += cp.quad_form(u[:, k], R)  # Penalti kontrol
    if k > 0:
        cost += cp.quad_form(u[:, k] - u[:, k - 1], delta_u_penalty)  # Penalti perubahan kontrol
    constraints += [x[:, k + 1] == A @ x[:, k] + B @ u[:, k] + w[:, k]]
    constraints += [u_min <= u[:, k], u[:, k] <= u_max]
    constraints += [cp.norm(w[:, k], 'inf') <= 0.2]  # Batas gangguan

# Definisi problem
problem = cp.Problem(cp.Minimize(cost), constraints)

# Eksekusi optimisasi
problem.solve()

# Output solusi
print("Optimal Control Inputs:", u.value)
