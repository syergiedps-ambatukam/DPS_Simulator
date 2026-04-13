import numpy as np
from scipy.optimize import minimize

# =========================
# 1. PARAMETER
# =========================

# Desired force & moment
f_x = 10
f_y = 5
m_z = 3

# Posisi thruster
positions = np.array([
    [1, 1],
    [1, -1],
    [-1, 1],
    [-1, -1]
])

# Previous angle (radian)
theta_prev = np.radians([0, 0, 0, 0])

# =========================
# 2. FUNCTION
# =========================

def angle_diff(theta, theta_prev):
    """Wrap angle difference biar ga salah (circular)"""
    return np.arctan2(np.sin(theta - theta_prev),
                      np.cos(theta - theta_prev))


def objective(x):
    F1, F2, F3, F4, t1, t2, t3, t4 = x

    # =========================
    # FORCE
    # =========================
    fx = F1*np.cos(t1) + F2*np.cos(t2) + F3*np.cos(t3) + F4*np.cos(t4)
    fy = F1*np.sin(t1) + F2*np.sin(t2) + F3*np.sin(t3) + F4*np.sin(t4)

    # =========================
    # MOMENT
    # =========================
    mz = (
        positions[0][0]*F1*np.sin(t1) - positions[0][1]*F1*np.cos(t1) +
        positions[1][0]*F2*np.sin(t2) - positions[1][1]*F2*np.cos(t2) +
        positions[2][0]*F3*np.sin(t3) - positions[2][1]*F3*np.cos(t3) +
        positions[3][0]*F4*np.sin(t4) - positions[3][1]*F4*np.cos(t4)
    )

    # =========================
    # ERROR TRACKING
    # =========================
    error = (f_x - fx)**2 + (f_y - fy)**2 + (m_z - mz)**2

    # =========================
    # PENALTI ENERGI
    # =========================
    lambda_F = 0
    penalty_F = lambda_F * (F1**2 + F2**2 + F3**2 + F4**2)

    # =========================
    # PENALTI PERUBAHAN SUDUT
    # =========================
    lambda_theta = 0.01

    theta = np.array([t1, t2, t3, t4])
    dtheta = angle_diff(theta, theta_prev)

    penalty_theta = lambda_theta * np.sum(dtheta**2)

    # =========================
    # TOTAL COST
    # =========================
    J = error + penalty_F + penalty_theta

    return J


# =========================
# 3. INITIAL GUESS
# =========================
x0 = np.array([
    5, 5, 5, 5,      # F1-F4
    0, 0, 0, 0       # theta1-theta4
])

# =========================
# 4. BOUNDS
# =========================
bounds = [
    (0, 10), (0, 10), (0, 10), (0, 10),      # F
    (0, 2*np.pi), (0, 2*np.pi), (0, 2*np.pi), (0, 2*np.pi)  # theta
]

# =========================
# 5. SOLVE NLP
# =========================
result = minimize(objective, x0, bounds=bounds)

# =========================
# 6. HASIL
# =========================
F_opt = result.x[:4]
theta_opt = result.x[4:]

print("=== HASIL OPTIMASI ===")
print("F:", np.round(F_opt, 3))
print("Theta (deg):", np.round(np.degrees(theta_opt), 2))

# =========================
# 7. VALIDASI
# =========================
fx_calc = np.sum(F_opt * np.cos(theta_opt))
fy_calc = np.sum(F_opt * np.sin(theta_opt))

mz_calc = np.sum([
    positions[i][0]*F_opt[i]*np.sin(theta_opt[i]) -
    positions[i][1]*F_opt[i]*np.cos(theta_opt[i])
    for i in range(4)
])

print("\n=== VALIDASI ===")
print("fx:", round(fx_calc, 3), "| target:", f_x)
print("fy:", round(fy_calc, 3), "| target:", f_y)
print("mz:", round(mz_calc, 3), "| target:", m_z)

print("\nError:")
print("fx error:", abs(f_x - fx_calc))
print("fy error:", abs(f_y - fy_calc))
print("mz error:", abs(m_z - mz_calc))
