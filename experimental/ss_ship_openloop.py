import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, lsim

# Parameter sistem

'''
m = np.array([[2.0, 0.1, 0.2], [0.1, 2.5, 0.3], [0.2, 0.3, 3.0]])  # matriks massa (3x3)
c = np.array([[0.5, 0.1, 0.0], [0.1, 0.6, 0.2], [0.0, 0.2, 0.7]])  # matriks redaman (3x3)
d = np.array([[0.2, 0.0, 0.1], [0.0, 0.3, 0.0], [0.1, 0.0, 0.4]])  # matriks gesekan (3x3)
'''


############ Model Kinetik ################################

print("==== Kinetik =======")
xg = 0.5 #posisi x center of gravity
yg = 0.4 #posisi y center of gravity
m = 27 #massa kapal
r = 0 #posisi arah surge / kecepatan sudut (psi_dot)
Iz = 0 #momen inersia akibat percepatan sumbu y

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


#gaya akibat massa

'''
#dari thesis teguh

m = np.array([[m, 0, -m*yg], [0, m, m*xg], [-m*yg, m*xg, Iz]])
+ np.array([[-x_udot,0,0],[0,-y_vdot,-y_rdot],[0,-n_vdot,-n_rdot]])
print(m)
'''
#dari Thomas P. DeRensis
m = np.array([[m, -0.003, 0.001], [0.002, m, m*xg], [-0.005, m*xg, Iz]])
+ np.array([[-x_udot,-0.002,0.003],[-0.003,y_vdot,y_rdot],[-0.001,n_vdot,n_rdot]])
print(m)


#gaya akibat drag
d = np.array([[x_u,-0.004,-0.002],
    [-0.003,y_v,y_r],
    [-0.001,n_v,n_r]]) 

print("d",d)


# Matriks State-Space

A = np.block([
    [np.zeros((3, 3)), np.eye(3)],
    [np.zeros((3, 3)), -np.linalg.inv(m) @ d]
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

# Matriks identitas
I = np.eye(A.shape[0])
T = 1

# Menghitung Ad dan Bd dengan Tustin
Ad = np.linalg.inv(I - (T/2) * A) @ (I + (T/2) * A)
Bd = np.linalg.inv(I - (T/2) * A) @ (T * B)

# Cd dan Dd tetap sama
Cd = C
Dd = D

# Cetak hasil
print("Ad:\n", Ad)
print("Bd:\n", Bd)
print("Cd:\n", Cd)
print("Dd:\n", Dd)



x = np.array([[0], [0], [0], [0], [0], [0]]) 
U = np.array([[0], [0], [0.0001]])

output_points_y1 = []
output_points_y2 = []
output_points_y3 = []
time_points = []

print("u",U)

t = 0
dt = 1

t_end = 100

#while True:
while t <= t_end:

    # Hitung keadaan berikutnya: x(k+1) = A*x(k) + B*u(k)
    x_next = Ad @ x * dt + Bd @ U * dt + x
    #print(x_next)

    # Hitung output: y(k) = C*x(k) + D*u(k)
    y = Cd @ x + Dd @ U
    
    print(y)
    
    time_points.append(t)
    output_points_y1.append(y[0, 0])  # Output y1 (posisi sudut)
    output_points_y2.append(y[1, 0])  # Output y2 (kecepatan sudut)
    output_points_y3.append(y[2, 0]) 
    
    t += dt
    x = x_next


# Visualisasi hasil simulasi
plt.figure(figsize=(10, 6))
plt.plot(time_points, output_points_y1, label="x")
plt.plot(time_points, output_points_y2, label="y")
plt.plot(time_points, output_points_y3, label="theta")
plt.title("Simulasi State-Space dps(3x3, 3 Input,6 state, 3 Output)")
plt.xlabel("Waktu (s)")
plt.ylabel("Output")
plt.grid()
plt.legend()
plt.show()

