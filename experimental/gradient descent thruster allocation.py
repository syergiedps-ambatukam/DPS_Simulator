import numpy as np

# Define the objective function (same as before)
def objective(x, f_x, f_y, m_z, positions):
    F_1, F_2, F_3, F_4, theta_1, theta_2, theta_3, theta_4 = x
    
    # Positions of the thrusters
    x1, y1 = positions[0]
    x2, y2 = positions[1]
    x3, y3 = positions[2]
    x4, y4 = positions[3]
    
    # Calculating total force in the x and y directions
    fx_calc = F_1 * np.cos(theta_1) + F_2 * np.cos(theta_2) + F_3 * np.cos(theta_3) + F_4 * np.cos(theta_4)
    fy_calc = F_1 * np.sin(theta_1) + F_2 * np.sin(theta_2) + F_3 * np.sin(theta_3) + F_4 * np.sin(theta_4)
    
    # Calculating total moment about the z-axis
    mz_calc = (x1 * F_1 * np.sin(theta_1) - y1 * F_1 * np.cos(theta_1)) + \
              (x2 * F_2 * np.sin(theta_2) - y2 * F_2 * np.cos(theta_2)) + \
              (x3 * F_3 * np.sin(theta_3) - y3 * F_3 * np.cos(theta_3)) + \
              (x4 * F_4 * np.sin(theta_4) - y4 * F_4 * np.cos(theta_4))
    
    # Squared differences between desired and calculated forces/moment
    error = (f_x - fx_calc)**2 + (f_y - fy_calc)**2 + (m_z - mz_calc)**2
    return error

# Gradient of the objective function (partial derivatives)
def gradient(x, f_x, f_y, m_z, positions):
    # Derivative w.r.t. F1, F2, F3, F4, theta1, theta2, theta3, theta4
    F_1, F_2, F_3, F_4, theta_1, theta_2, theta_3, theta_4 = x
    
    # Positions of the thrusters
    x1, y1 = positions[0]
    x2, y2 = positions[1]
    x3, y3 = positions[2]
    x4, y4 = positions[3]
    
    # Force and moment components
    fx_calc = F_1 * np.cos(theta_1) + F_2 * np.cos(theta_2) + F_3 * np.cos(theta_3) + F_4 * np.cos(theta_4)
    fy_calc = F_1 * np.sin(theta_1) + F_2 * np.sin(theta_2) + F_3 * np.sin(theta_3) + F_4 * np.sin(theta_4)
    mz_calc = (x1 * F_1 * np.sin(theta_1) - y1 * F_1 * np.cos(theta_1)) + \
              (x2 * F_2 * np.sin(theta_2) - y2 * F_2 * np.cos(theta_2)) + \
              (x3 * F_3 * np.sin(theta_3) - y3 * F_3 * np.cos(theta_3)) + \
              (x4 * F_4 * np.sin(theta_4) - y4 * F_4 * np.cos(theta_4))
    
    # Compute the error term
    error_fx = 2 * (fx_calc - f_x)
    error_fy = 2 * (fy_calc - f_y)
    error_mz = 2 * (mz_calc - m_z)
    
    # Partial derivatives for each parameter
    dF_1 = error_fx * np.cos(theta_1) + error_fy * np.sin(theta_1) + error_mz * (x1 * np.cos(theta_1) + y1 * np.sin(theta_1))
    dF_2 = error_fx * np.cos(theta_2) + error_fy * np.sin(theta_2) + error_mz * (x2 * np.cos(theta_2) + y2 * np.sin(theta_2))
    dF_3 = error_fx * np.cos(theta_3) + error_fy * np.sin(theta_3) + error_mz * (x3 * np.cos(theta_3) + y3 * np.sin(theta_3))
    dF_4 = error_fx * np.cos(theta_4) + error_fy * np.sin(theta_4) + error_mz * (x4 * np.cos(theta_4) + y4 * np.sin(theta_4))
    
    dtheta_1 = error_fx * (-F_1 * np.sin(theta_1)) + error_fy * (F_1 * np.cos(theta_1)) + error_mz * (x1 * F_1 * np.cos(theta_1) - y1 * F_1 * np.sin(theta_1))
    dtheta_2 = error_fx * (-F_2 * np.sin(theta_2)) + error_fy * (F_2 * np.cos(theta_2)) + error_mz * (x2 * F_2 * np.cos(theta_2) - y2 * F_2 * np.sin(theta_2))
    dtheta_3 = error_fx * (-F_3 * np.sin(theta_3)) + error_fy * (F_3 * np.cos(theta_3)) + error_mz * (x3 * F_3 * np.cos(theta_3) - y3 * F_3 * np.sin(theta_3))
    dtheta_4 = error_fx * (-F_4 * np.sin(theta_4)) + error_fy * (F_4 * np.cos(theta_4)) + error_mz * (x4 * F_4 * np.cos(theta_4) - y4 * F_4 * np.sin(theta_4))
    
    return np.array([dF_1, dF_2, dF_3, dF_4, dtheta_1, dtheta_2, dtheta_3, dtheta_4])

# Gradient Descent
def gradient_descent(f_x, f_y, m_z, positions, x0, learning_rate=0.01, tolerance=1e-6, max_iters=1000):
    x = x0
    for i in range(max_iters):
        grad = gradient(x, f_x, f_y, m_z, positions)
        x_new = x - learning_rate * grad
        # Check for convergence
        if np.linalg.norm(x_new - x) < tolerance:
            break
        x = x_new
    return x

# Given data (desired force and moment, positions)
f_x = 10  # desired force in x direction
f_y = 5   # desired force in y direction
m_z = 2   # desired moment about z-axis
positions = np.array([
    [1, 1],  # Thruster 1 position
    [1, -1], # Thruster 2 position
    [-1, 1], # Thruster 3 position
    [-1, -1] # Thruster 4 position
])

# Initial guess for magnitudes and angles (in radians)
x0 = np.array([5, 5, 5, 5, np.pi/4, np.pi/4, np.pi/4, np.pi/4])

# Run gradient descent to find the optimal solution
optimal_x = gradient_descent(f_x, f_y, m_z, positions, x0)

# Extract results
F_1_opt, F_2_opt, F_3_opt, F_4_opt, theta_1_opt, theta_2_opt, theta_3_opt, theta_4_opt = optimal_x


fx_calc = F_1_opt * np.cos(theta_1_opt) + F_2_opt * np.cos(theta_2_opt) + F_3_opt * np.cos(theta_3_opt) + F_4_opt * np.cos(theta_4_opt)
fy_calc = F_1_opt * np.sin(theta_1_opt) + F_2_opt * np.sin(theta_2_opt) + F_3_opt * np.sin(theta_3_opt) + F_4_opt * np.sin(theta_4_opt)
mz_calc = (positions[0][0] * F_1_opt * np.sin(theta_1_opt) - positions[0][1] * F_1_opt * np.cos(theta_1_opt)) + \
          (positions[1][0] * F_2_opt * np.sin(theta_2_opt) - positions[1][1] * F_2_opt * np.cos(theta_2_opt)) + \
          (positions[2][0] * F_3_opt * np.sin(theta_3_opt) - positions[2][1] * F_3_opt * np.cos(theta_3_opt)) + \
          (positions[3][0] * F_4_opt * np.sin(theta_4_opt) - positions[3][1] * F_4_opt * np.cos(theta_4_opt))


# Error calculation
error_fx = abs(f_x - fx_calc)
error_fy = abs(f_y - fy_calc)
error_mz = abs(m_z - mz_calc)

print(f"Error in Force (fx, fy): {error_fx:.2f}, {error_fy:.2f}")

# Print results
print(f"Optimal F1: {F_1_opt:.2f}, Optimal F2: {F_2_opt:.2f}, Optimal F3: {F_3_opt:.2f}, Optimal F4: {F_4_opt:.2f}")
print(f"Optimal theta1 (in degrees): {np.degrees(theta_1_opt):.2f}, Optimal theta2 (in degrees): {np.degrees(theta_2_opt):.2f}")
print(f"Optimal theta3 (in degrees): {np.degrees(theta_3_opt):.2f}, Optimal theta4 (in degrees): {np.degrees(theta_4_opt):.2f}")