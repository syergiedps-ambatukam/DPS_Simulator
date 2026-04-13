import numpy as np
import math
from scipy.optimize import minimize


ly1 = 0.25
lx1 = 1

ly2 = -0.25
lx2 = 1

ly3 = -0.25
lx3 = -1

ly4 = 0.25
lx4 = -1

steering1 = 90
steering2 = 0
steering3 = 0
steering4 = 0

T_total = np.array([0, 0, 0, 0, 0, 0, 0, 0])
T1 = 0
T2 = 0
T3 = 0
T4 = 0

tau = np.array([3, 2, 1])


###################MAIN PROGRAM###############################################



T_linear = np.array([[1, 0, 1, 0, 1, 0, 1, 0],   # Menambah kolom untuk F_x4
              [0, 1, 0, 1, 0, 1, 0, 1],   # Menambah kolom untuk F_y4
              [-ly1, lx1, -ly2, lx2, -ly3, lx3, -ly4, lx4]])  # Menyesuaikan gaya kontrol

T_transpose = T_linear.T
W = np.eye(8)
W_inv = np.linalg.inv(W)
TWT_inv = np.linalg.inv(T_linear @ W_inv @ T_transpose)
T_pseudo_inverse = W_inv @ T_transpose @ TWT_inv

print(tau)

T_total = T_pseudo_inverse @ tau

try:
    steering1 = math.atan2(float(T_total[1]),float(T_total[0])) * 180/math.pi
except:
    steering1 = 90
    
gas_throttle1_psuedo = math.sqrt(float(T_total[1])**2 + float(T_total[0])**2)


try:
    steering2= math.atan2(float(T_total[3]),float(T_total[2])) * 180/math.pi
except:
    steering2 = 90

gas_throttle2_psuedo = math.sqrt(float(T_total[3])**2 + float(T_total[2])**2)

try:
    steering3 = math.atan2(float(T_total[5]),float(T_total[4])) * 180/math.pi
except:
    steering3 = 90
gas_throttle3_psuedo = math.sqrt(float(T_total[5])**2 + float(T_total[4])**2)


try:
    steering4 = math.atan2(float(T_total[7]),float(T_total[6])) * 180/math.pi
except:
    steering4 = 90
gas_throttle4_psuedo = math.sqrt(float(T_total[7])**2 + float(T_total[6])**2)


#print(T_total)

#print(steering1, steering2, steering3, steering4)


T_nonlinear = np.array ([[np.cos(np.deg2rad(steering1)), np.cos(np.deg2rad(steering2)), np.cos(np.deg2rad(steering3)), np.cos(np.deg2rad(steering4))],
                      [np.sin(np.deg2rad(steering1)), np.sin(np.deg2rad(steering2)), np.sin(np.deg2rad(steering3)), np.sin(np.deg2rad(steering4))],
                      [(lx1 * np.cos(np.deg2rad(steering1)) - ly1 * np.sin(np.deg2rad(steering1))), (lx2 * np.cos(np.deg2rad(steering2)) - ly2 * np.sin(np.deg2rad(steering2))), (lx3 * np.cos(np.deg2rad(steering3)) - ly3 * np.sin(np.deg2rad(steering3))), (lx4 * np.cos(np.deg2rad(steering4)) - ly4 * np.sin(np.deg2rad(steering4)))  ]])

#print(T_nonlinear)


tau_nonlinear = T_nonlinear @ np.array([gas_throttle1_psuedo, gas_throttle2_psuedo, gas_throttle3_psuedo, gas_throttle4_psuedo])

print(T_linear @ T_total)
print(tau_nonlinear)



