import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, lsim

# Parameter sistem
m = np.array([[2.0, 0.1, 0.2], [0.1, 2.5, 0.3], [0.2, 0.3, 3.0]])  # matriks massa (3x3)
c = np.array([[0.5, 0.1, 0.0], [0.1, 0.6, 0.2], [0.0, 0.2, 0.7]])  # matriks redaman (3x3)
d = np.array([[0.2, 0.0, 0.1], [0.0, 0.3, 0.0], [0.1, 0.0, 0.4]])  # matriks gesekan (3x3)

# Matriks State-Space
A = np.block([
    [np.zeros((3, 3)), np.eye(3)],
    [-np.linalg.inv(m) @ c, -np.linalg.inv(m) @ d]
])
B = np.block([
    [np.zeros((3, 3))],
    [np.linalg.inv(m)]
])
C = np.block([
    [np.eye(3), np.zeros((3, 3))]
])
D = np.zeros((3, 3))

print("A")
print(A)

print("B")
print(B)

print("C")
print(C)


print("D")
print(D)

# Waktu simulasi
time = np.linspace(0, 10, 1000)  # 0 hingga 10 detik dengan 1000 titik

# Input (step function)
u = np.ones((len(time), 3))  # Step input: vektor ukuran 3 untuk setiap waktu

# Sistem LTI
system = lti(A, B, C, D)

# Simulasi step response
_, y_out, _ = lsim(system, U=u, T=time)

# Plot hasil
plt.figure(figsize=(8, 5))
for i in range(3):
    plt.plot(time, y_out[:, i], label=f"Response (v{i+1})")
plt.title("Step Response of the System (3x3 State-Space)")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (v)")
plt.grid()
plt.legend()
plt.show()
