import numpy as np
import math

ly1 = 0.25
lx1 = 1

ly2 = -0.25
lx2 = 1

ly3 = -0.25
lx3 = -1

ly4 = -0.25
lx4 = 1


T = np.array([[1, 0, 1, 0, 1, 0, 1, 0],   # Menambah kolom untuk F_x4
              [0, 1, 0, 1, 0, 1, 0, 1],   # Menambah kolom untuk F_y4
              [-ly1, lx1, -ly2, lx2, -ly3, lx3, -ly4, lx4]])  # Menyesuaikan gaya kontrol

T_transpose = T.T
W = np.eye(8)
W_inv = np.linalg.inv(W)
TWT_inv = np.linalg.inv(T @ W_inv @ T_transpose)
T_pseudo_inverse = W_inv @ T_transpose @ TWT_inv
tau_control = np.array([0, 0, 10])

f = T_pseudo_inverse @ tau_control
print(tau_control)
print("==========")

print(f)


try:
    steering1 = math.atan2(float(f[1]),float(f[0])) * 180/math.pi
except:
    steering1 = 90

gas_throttle1_psuedo = math.sqrt(float(f[1])**2 + float(f[0])**2)


try:
    steering2= math.atan2(float(f[3]),float(f[2])) * 180/math.pi
except:
    steering2 = 90

gas_throttle2_psuedo = math.sqrt(float(f[3])**2 + float(f[2])**2)

try:
    steering3 = math.atan2(float(f[5]),float(f[4])) * 180/math.pi
except:
    steering3 = 90
gas_throttle3_psuedo = math.sqrt(float(f[5])**2 + float(f[4])**2)


try:
    steering4 = math.atan2(float(f[7]),float(f[6])) * 180/math.pi
except:
    steering4 = 90
gas_throttle4_psuedo = math.sqrt(float(f[7])**2 + float(f[6])**2)


fx1_real = gas_throttle1_psuedo * math.cos(steering1 * math.pi/180)
fy1_real = gas_throttle1_psuedo * math.sin(steering1 * math.pi/180)

fx2_real = gas_throttle2_psuedo * math.cos(steering2 * math.pi/180)
fy2_real = gas_throttle2_psuedo * math.sin(steering2 * math.pi/180)

fx3_real = gas_throttle3_psuedo * math.cos(steering3 * math.pi/180)
fy3_real = gas_throttle3_psuedo * math.sin(steering3 * math.pi/180)

fx4_real = gas_throttle4_psuedo * math.cos(steering4 * math.pi/180)
fy4_real = gas_throttle4_psuedo * math.sin(steering4 * math.pi/180)

f = [fx1_real, fy1_real, fx2_real, fy2_real, fx3_real, fy3_real, fx4_real, fy4_real]

print(f)

print("=======")

tau = np.round(T@f)



print(tau)