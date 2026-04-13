import numpy as np

# =========================
# KONFIGURASI THRUSTER
# =========================
# posisi thruster (meter)
lx = np.array([0.8, -0.8, -0.8, 0.8])
ly = np.array([0.6, 0.6, -0.6, -0.6])

n = 4

# =========================
# BUILD MATRIX B_u
# =========================
B = np.zeros((3, 2*n))

for i in range(n):
    # ux contribution
    B[0, 2*i]   = 1          # surge
    B[1, 2*i]   = 0          # sway
    B[2, 2*i]   = -ly[i]     # yaw

    # uy contribution
    B[0, 2*i+1] = 0
    B[1, 2*i+1] = 1
    B[2, 2*i+1] = lx[i]

# =========================
# TARGET FORCE (tau)
# =========================
tau = np.array([10, 5, 2])   # [Fx, Fy, Mz]

# =========================
# PREVIOUS CONTROL (u_prev)
# =========================
u_prev = np.zeros(2*n)

# =========================
# QP PARAMETER
# =========================
Q = np.eye(2*n)
rho = 5.0   # penalti smoothness

H = Q + rho * np.eye(2*n)
f = -rho * u_prev

# =========================
# SOLVE KKT SYSTEM
# =========================
KKT = np.block([
    [H, B.T],
    [B, np.zeros((3,3))]
])

rhs = np.concatenate([-f, tau])

sol = np.linalg.solve(KKT, rhs)

u = sol[:2*n]

# =========================
# RECOVER f dan alpha
# =========================
f_thruster = []
alpha_thruster = []

for i in range(n):
    ux = u[2*i]
    uy = u[2*i+1]

    f_i = np.sqrt(ux**2 + uy**2)
    alpha_i = np.arctan2(uy, ux)

    f_thruster.append(f_i)
    alpha_thruster.append(alpha_i)

# =========================
# PRINT RESULT
# =========================
for i in range(n):
    print(f"Thruster {i+1}:")
    print(f"  f     = {f_thruster[i]:.3f} N")
    print(f"  alpha = {np.degrees(alpha_thruster[i]):.2f} deg")
    
    
# =========================
# CEK TAU HASIL
# =========================
tau_generated = B @ u
error = tau_generated - tau

print("\n=== HASIL TAU ===")
print(f"Tau desired   : {tau}")
print(f"Tau generated : {tau_generated}")

print("\n=== ERROR ===")
print(f"Error         : {error}")
print(f"Norm error    : {np.linalg.norm(error):.6f}")