import numpy as np
import math

lx1, ly1 =  1.0, -0.25
lx2, ly2 = -1.0, -0.25
lx3, ly3 = -1.0,  0.25
lx4, ly4 =  1.0,  0.25


T = np.array([
    [1, 0, 1, 0, 1, 0, 1, 0],                      # ΣFx
    [0, 1, 0, 1, 0, 1, 0, 1],                      # ΣFy
    [-ly1, lx1, -ly2, lx2, -ly3, lx3, -ly4, lx4]  # ΣMz = lx*Fy - ly*Fx
])


W = np.eye(8)
T_pseudo_inverse = W @ T.T @ np.linalg.inv(T @ W @ T.T)


tau_control = np.array([0.0, 0.0, 10.0])   # target yaw murni

f = T_pseudo_inverse @ tau_control

try:
    steering1 = math.atan2(float(f[1]),float(f[0])) * 180/math.pi
except:
    steering1 = 90                
gas_throttle1 = math.sqrt(float(f[1])**2 + float(f[0])**2)


try:
    steering3 = math.atan2(float(f[3]),float(f[2])) * 180/math.pi
except:
    steering3 = 90
gas_throttle3 = math.sqrt(float(f[3])**2 + float(f[2])**2)

try:
    steering4 = math.atan2(float(f[5]),float(f[4])) * 180/math.pi
except:
    steering4 = 90
gas_throttle4 = math.sqrt(float(f[5])**2 + float(f[4])**2)


try:
    steering2 = math.atan2(float(f[7]),float(f[6])) * 180/math.pi
except:
    steering2 = 90
gas_throttle2 = math.sqrt(float(f[7])**2 + float(f[6])**2)
            



print("f (Fx1, Fy1, ..., Fx4, Fy4) =")
print(f)

tau_real = T @ f

print("tau_real =")
print(tau_real)
