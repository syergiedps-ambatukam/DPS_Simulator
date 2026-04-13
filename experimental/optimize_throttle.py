import numpy as np
from scipy.optimize import lsq_linear


def allocate_throttle(
    tau_target,          # [Fx, Fy, Mz]
    steering_rad,        # azimuth angles (rad)
    lx, ly,              # thruster positions
    T_min=0.0,
    T_max=5.0,
    tol=1e-2
):
    """
    Thruster allocation with feasibility detection

    Returns:
        dict with:
        - T
        - tau_real
        - error
        - error_norm
        - rank_B
        - status
    """

    n = len(steering_rad)
    B = np.zeros((3, n))

    for i in range(n):
        c = np.cos(steering_rad[i])
        s = np.sin(steering_rad[i])

        B[0, i] = c
        B[1, i] = s
        B[2, i] = lx[i]*s - ly[i]*c

    bounds = (np.ones(n)*T_min, np.ones(n)*T_max)

    res = lsq_linear(B, tau_target, bounds=bounds)

    T = res.x
    tau_real = B @ T

    error = tau_target - tau_real
    error_norm = np.linalg.norm(error)

    rank_B = np.linalg.matrix_rank(B)

    if error_norm < tol:
        status = "FEASIBLE"
    else:
        status = "INFEASIBLE"

    return {
        "T": T,
        "tau_real": tau_real,
        "error": error,
        "error_norm": error_norm,
        "rank_B": rank_B,
        "status": status
    }



steering = np.deg2rad([-90, -90, 45, -45])

lx = np.array([1, 1, -1, 1])
ly = np.array([0.25, -0.25, -0.25, -0.25])

tau_target = np.array([4, 0, 0.5])

result = allocate_throttle(
    tau_target,
    steering,
    lx,
    ly,
    T_min=0,
    T_max=5
)

print("Status      :", result["status"])
print("Rank B      :", result["rank_B"])
print("Throttle    :", result["T"])
print("Tau real    :", result["tau_real"])
print("Error       :", result["error"])
print("Error norm  :", result["error_norm"])
