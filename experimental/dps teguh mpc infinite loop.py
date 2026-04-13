import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import time

plt.ion()  # Mode interaktif
fig, ax = plt.subplots()

x_data, y1_data, y2_data, y3_data, y4_data, y5_data, y6_data = [], [], [], [], [], [], []
line1, = ax.plot([], [], 'b-', label='Channel 1')  # Garis biru
line2, = ax.plot([], [], 'r--', label='Channel 2')  # Garis merah

line3, = ax.plot([], [], 'g-', label='Channel 3')  # Garis biru
line4, = ax.plot([], [], 'r--', label='Channel 4')  # Garis merah

line5, = ax.plot([], [], 'y-', label='Channel 5')  # Garis biru
line6, = ax.plot([], [], 'r--', label='Channel 6')  # Garis merah


ax.legend()
i = 0

############ Model Kinetik ################################

print("==== Kinetik =======")
xg = 0.5  # posisi x center of gravity
yg = 0.4  # posisi y center of gravity
mass = 27  # massa kapal
r = 0  # posisi arah surge / kecepatan sudut (psi_dot)
Iz = 0  # momen inersia akibat percepatan sumbu y

x_u = 0.9
y_v = 0.6
n_r = 0.3
y_r = 0.1
n_v = 0.2

x_udot = 0.9
y_vdot = 0.6
y_rdot = 0.7
n_vdot = 0.3
n_rdot = 0.4
u = 0
v = 0
r = 0

# gaya akibat massa
m = np.array([[mass, -0, 0], [0.0, mass, mass * xg], [-0.00, mass * xg, Iz]]) + np.array(
    [[-x_udot, -0.00, 0.00], [-0.00, y_vdot, y_rdot], [-0.00, n_vdot, n_rdot]])
print(m)

y_dot = 0
x_dot = 0

# gaya akibat coriolis
c = np.array([[0, 0, -mass * (xg * r + float(y_dot))],
              [0, 0, -mass * (yg * r + float(x_dot))],
              [-mass * (xg * r + float(y_dot)), -mass * (yg * r + float(x_dot)), 0]]) + np.array(
    [[0, 0, -y_vdot * float(y_dot) - ((y_rdot + n_vdot) / 2) * r],
     [0, 0, x_udot * float(x_dot)],
     [-y_vdot * float(y_dot) - ((y_rdot + n_vdot) / 2) * r, x_udot * float(x_dot), 0]])

# gaya akibat drag
d = np.array([[x_u, -0.00, -0.00],
              [-0.00, y_v, y_r],
              [-0.00, n_v, n_r]])

print("d", d)

# Matriks State-Space


A = np.block([
    [np.zeros((3, 3)), np.eye(3)],
    [np.zeros((3, 3)), -np.linalg.inv(m) @ d]
])
'''

A = np.block([
    [np.zeros((3, 3)), np.eye(3)],
    [-np.linalg.inv(m) @ d, -np.linalg.inv(m) @ c]
])
'''
B = np.block([
    [np.zeros((3, 3))],
    [np.linalg.inv(m)]
])
C = np.block([
    [np.eye(3), np.zeros((3, 3))]
])
D = np.zeros((3, 3))


print("continous state space")
print("A")
print(str(A))

print("B")
print(B)

print("C")
print(C)


print("D")
print(D)

I = np.eye(A.shape[0])
T = 1

# Menghitung Ad dan Bd dengan Tustin
A = np.linalg.inv(I - (T/2) * A) @ (I + (T/2) * A)
B = np.linalg.inv(I - (T/2) * A) @ (T * B)

# Cd dan Dd tetap sama
C = C
D = D


print("discrete state space")
print("A")
print(str(A))

print("B")
print(B)

print("C")
print(C)


print("D")
print(D)


# ===== Parameter MPC =====
N = 10  # Prediction horizon
#Q =  10000
Q = np.diag([10, 10, 10])  # Penalty for output error (adjusted for 3 outputs)
R = np.diag([0.1, 0.1, 0.1])  # Penalty for control effort (adjusted for 3 inputs)
delta_u_penalty = np.diag([10, 10, 10])  # Penalti perubahan kontrol (adjusted for 3 inputs)
u_min, u_max = -1000.0, 1000.0  # Batas kontrol

# ===== Variabel Simulasi =====
x0 = np.array([[5], [5], [5], [0], [0],[0]])  # Status awal
print("x0 =", x0)
predicted_states = []
applied_inputs = []
time_steps = []
y = np.array([[0], [0.0], [-1000]])

print("=========================")


while True:
    y_ref = np.array([10, 0, 0]).reshape(-1, 1)  # Reshape untuk dimensi (3, 1)

    # ===== Variabel Optimisasi =====
    x = cp.Variable((A.shape[0], N + 1))  # State variables
    u = cp.Variable((B.shape[1], N))  # Control inputs

    # ===== Fungsi Biaya dan Kendala =====
    cost = 0
    constraints = []

    for k in range(N):
        cost += cp.quad_form(C @ x[:, k] - y_ref.flatten(), Q)  # Penalti error (gunakan y_ref yang sudah direshape)
        cost += cp.quad_form(u[:, k], R)  # Penalti kontrol
        if k > 0:
            cost += cp.quad_form(u[:, k] - u[:, k - 1], delta_u_penalty)  # Penalti perubahan kontrol
        constraints += [x[:, k + 1] == A @ x[:, k] + B @ u[:, k]]
        constraints += [u_min <= u[:, k], u[:, k] <= u_max]

    # Status awal
    constraints += [x[:, 0] == x0.flatten()]

    # Problem MPC
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve()

    # ===== Ambil Kontrol Optimal =====
    if problem.status != 'optimal':
        print(f"Solver failed at step {i}. Status: {problem.status}")
        break

    u_optimal = u.value[:, 0]

    # ===== Simulasikan Sistem =====
    x0 = A @ x0 + B @ u_optimal.reshape(-1, 1)
    #x0 = A @ x0 + B @ np.array([[0.0001], [0], [0]])
    y = C @ x0

    # Simpan Hasil
    predicted_states.append(y.flatten())
    applied_inputs.append(u_optimal)
    time_steps.append(i * 0.1)  # Assuming T = 0.1

    print(f"Setpoint: {y_ref.flatten()}, Sensor: {y.flatten()}, Input: {u_optimal.reshape(-1, 1)}")
    
    x_data.append(i)
    y1_data.append(y.flatten()[0])  # Data untuk channel 1
    y2_data.append(y_ref.flatten()[0])  # Data untuk channel 2
    y3_data.append(y.flatten()[1])
    y4_data.append(y_ref.flatten()[1])
    
    y5_data.append(y.flatten()[2])
    y6_data.append(y_ref.flatten()[2])


    # Menjaga hanya 20 data terakhir
    x_data = x_data[-20:]
    y1_data = y1_data[-20:]
    y2_data = y2_data[-20:]
    
    y3_data = y3_data[-20:]
    y4_data = y4_data[-20:]

    y5_data = y5_data[-20:]
    y6_data = y6_data[-20:]

    line1.set_xdata(x_data)
    line1.set_ydata(y1_data)
    
    line2.set_xdata(x_data)
    line2.set_ydata(y2_data)
    
    
    line3.set_xdata(x_data)
    line3.set_ydata(y3_data)
    
    line4.set_xdata(x_data)
    line4.set_ydata(y4_data)
    
    
    line5.set_xdata(x_data)
    line5.set_ydata(y5_data)
    
    line6.set_xdata(x_data)
    line6.set_ydata(y6_data)

    # ===== Perbaikan untuk ax.set_xlim() =====
    if len(x_data) > 1:
        ax.set_xlim(min(x_data), max(x_data))
    else:
        ax.set_xlim(x_data[0] - 1, x_data[0] + 1)  # Menambahkan margin jika hanya ada satu titik

    ax.relim()
    ax.autoscale_view()

    plt.draw()
    plt.pause(0.1)

    i += 1
    time.sleep(0.1)
