import numpy as np
from scipy.optimize import minimize

# Define the objective function
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

# Given data (desired force and moment, positions)
f_x = 10  # desired force in x direction
f_y = 5   # desired force in y direction
m_z = 2   # desired moment about z-axis

# Positions of the thrusters (x, y coordinates)
positions = np.array([
    [1, 1],  # Thruster 1 position
    [1, -1], # Thruster 2 position
    [-1, 1], # Thruster 3 position
    [-1, -1] # Thruster 4 position
])

# Initial guess for magnitudes and angles (in radians)
x0 = np.array([5, 5, 5, 5, 0, 0, 0, 0])

# Bounds for the variables (magnitudes are positive, angles between 0 and 2*pi)
bounds = [(0, None), (0, None), (0, None), (0, None), (0, 2*np.pi), (0, 2*np.pi), (0, 2*np.pi), (0, 2*np.pi)]

# Solve the optimization problem
result = minimize(objective, x0, args=(f_x, f_y, m_z, positions), bounds=bounds)

# Extract results
F_1_opt, F_2_opt, F_3_opt, F_4_opt, theta_1_opt, theta_2_opt, theta_3_opt, theta_4_opt = result.x

# Print optimal magnitudes and angles in degrees
print(f"Optimal F1: {F_1_opt:.2f}, Optimal F2: {F_2_opt:.2f}, Optimal F3: {F_3_opt:.2f}, Optimal F4: {F_4_opt:.2f}")
print(f"Optimal theta1 (in degrees): {np.degrees(theta_1_opt):.2f}, Optimal theta2 (in degrees): {np.degrees(theta_2_opt):.2f}")
print(f"Optimal theta3 (in degrees): {np.degrees(theta_3_opt):.2f}, Optimal theta4 (in degrees): {np.degrees(theta_4_opt):.2f}")

# Calculate total force and error
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

# Print total force, desired value, and error value
total_force = np.sqrt(fx_calc**2 + fy_calc**2)
print(f"\nCalculated Total Force: {total_force:.2f}")
print(f"Desired Total Force: {np.sqrt(f_x**2 + f_y**2):.2f}")
print(f"Error in Force (fx, fy): {error_fx:.2f}, {error_fy:.2f}")
print(f"Calculated Moment: {mz_calc:.2f}")
print(f"Desired Moment: {m_z:.2f}")
print(f"Error in Moment (m_z): {error_mz:.2f}")