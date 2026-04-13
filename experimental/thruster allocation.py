import numpy as np

# ===== INPUT =====
alpha = np.deg2rad([0, 80, 180, 270])   # sudut thruster (deg → rad)
lx = np.array([ 2.0,  0.0, -2.0,  0.0]) # posisi x thruster (m) ver 2
ly = np.array([ 0.0,  2.0,  0.0, -2.0]) # posisi y thruster (m) ver 2

# gaya thruster
#F = np.array([100, 100, 100, 100])     # N ver1
F = np.array([0, 20, 100, 0, 100, 0, 100, 0])


# ===== MATRIX B =====
'''
ver 1
B = np.vstack([
    np.cos(alpha),
    np.sin(alpha),
    ly * np.cos(alpha) + lx * np.sin(alpha)
])
'''

ly1 = -0.25
lx1 = 1

ly2 = -0.25
lx2 = -1

ly3 = 0.25
lx3 = -1

ly4 = 0.25
lx4 = 1

B = np.array([[1, 0, 1, 0, 1, 0, 1, 0],   # Menambah kolom untuk F_x4
              [0, 1, 0, 1, 0, 1, 0, 1],   # Menambah kolom untuk F_y4
              [ly1, lx1, ly2, lx2, ly3, lx3, ly4, lx4]])  # Menyesuaikan gaya kontrol


# ===== RESULTANT FORCE & MOMENT =====
tau = B @ F

Fx, Fy, Mz = tau

print("Fx =", Fx)
print("Fy =", Fy)
print("Mz =", Mz)
