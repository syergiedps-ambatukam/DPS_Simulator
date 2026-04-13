import numpy as np

# Define the sliding mode control parameters for a 3x3 system
class SlidingModeControl:
    def __init__(self, M1, C1, D1, J, R, E, Lambda):
        self.M1 = M1
        self.C1 = C1
        self.D1 = D1
        self.J = J
        self.R = R
        self.E = E
        self.Lambda = Lambda
    
    def sat(self, value):
        """Saturation function."""
        # Ensure the result is a 3x1 vector
        return np.clip(value, -1, 1)
    
    def model_based_control(self, eta_dot, v_dot):
        """Compute the model-based control part for 3x1 tau."""
        # Result should be a 3x1 vector: M1*eta_dot + C1(v_dot)*v_dot + D1(v_dot)*v_dot
        return np.dot(self.M1, eta_dot) + np.dot(self.C1(v_dot), v_dot) + np.dot(self.D1(v_dot), v_dot)
    
    def switching_control(self, s):
        """Compute the switching control part for 3x1 tau."""
        # J(s) is a 3x3 matrix, R is 3x3 matrix, s is a 3x1 vector
        J_s = self.J(s)  # J(s) should return a 3x3 matrix
        E_inv_s = np.linalg.inv(self.E) @ s  # E^-1 * s is a 3x1 vector
        # Now apply the correct matrix multiplication and saturation
        return np.dot(J_s, self.R) @ self.sat(E_inv_s)  # Ensure this is a 3x1 vector
    
    def control_law(self, eta_dot, v_dot, s):
        """Compute the full sliding mode control law, returning a 3x1 vector."""
        tau_model_based = self.model_based_control(eta_dot, v_dot)
        tau_switching = self.switching_control(s)
        return tau_model_based - tau_switching

# Example usage for a 3x3 system with 3x1 tau

# M1, C1, D1 are 3x3 matrices for the system dynamics
M1 = np.eye(3)  # 3x3 identity matrix as an example
C1 = lambda v: np.eye(3)  # Example function returning 3x3 identity matrix
D1 = lambda v: np.eye(3)  # Example function returning 3x3 identity matrix
J = lambda v: np.eye(3)  # Example function returning 3x3 identity matrix
R = np.eye(3)  # 3x3 identity matrix for gain matrix
E = np.eye(3)  # 3x3 identity matrix for boundary layer thickness
Lambda = 1  # Example value for Lambda

# Create an instance of the sliding mode controller for a 3x3 system
smc = SlidingModeControl(M1, C1, D1, J, R, E, Lambda)

# Example state values (3x1 vectors)
eta_dot = np.array([0.5, 0.3, 0.2])  # 3x1 state derivative vector (example)
v_dot = np.array([0.4, 0.1, 0.3])  # 3x1 state derivative vector (example)
s = np.array([0.1, 0.2, 0.3])  # 3x1 sliding surface value (example)

# Compute the control law for the 3x1 tau
tau_smc = smc.control_law(eta_dot, v_dot, s)

print("Sliding Mode Control Output (3x1 tau):", tau_smc)
