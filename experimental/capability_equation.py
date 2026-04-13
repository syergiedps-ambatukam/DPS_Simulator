import numpy as np
from scipy.optimize import linprog

steering_array = np.array([-90, 180, 90, 0])
Fmax = np.array([10, 10, 10, 10])

theta = np.deg2rad(steering_array)
angles = np.arange(0, 361, 10)

deg = np.zeros(len(angles))
val = np.zeros(len(angles))

print("Arah |   F1    F2    F3    F4  | F_total")
print("------------------------------------------------")

for k in range(len(angles)):
    phi_deg = angles[k]
    phi = np.deg2rad(phi_deg)

    c = -np.cos(theta - phi)

    A_eq = [np.sin(theta - phi)]
    b_eq = [0]

    bounds = [(0, Fmax[i]) for i in range(4)]

    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if res.success:
        F = res.x
        F_total = np.sum(F * np.cos(theta - phi))

        print(f"{phi_deg:3d} | "
              f"{F[0]:5.2f} {F[1]:5.2f} {F[2]:5.2f} {F[3]:5.2f} | "
              f"{F_total:6.2f}")
    else:
        print(f"{phi_deg:3d} | No solution")
        F_total = 0

    deg[k] = phi_deg
    val[k] = F_total

print(deg)
print(val)