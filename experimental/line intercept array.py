import numpy as np
import matplotlib.pyplot as plt
import time


def ray_segment_intersection_system(x, y, P, theta_deg, plot=True):
    """
    Sistem lengkap:
    - Mencari titik potong ray dari P dengan sudut theta
    - Mengecek validasi arah dan segmen
    - Menampilkan hasil
    - Optional plotting
    """

    x = np.array(x)
    y = np.array(y)
    P = np.array(P)

    intersections = []

    theta_rad = np.radians(theta_deg)
    v_theta = np.array([np.cos(theta_rad), np.sin(theta_rad)])

    # ---------- HITUNG INTERSECTION ----------
    for i in range(len(x) - 1):
        A = np.array([x[i], y[i]])
        B = np.array([x[i + 1], y[i + 1]])

        v_AB = B - A
        M = np.column_stack((v_AB, -v_theta))
        rhs = P - A

        if np.linalg.matrix_rank(M) < 2:
            continue

        try:
            sol = np.linalg.solve(M, rhs)
            s = sol[0]
            intersection = A + s * v_AB

            # Validasi arah ray
            arah = intersection - P
            if np.dot(arah, v_theta) < 0:
                continue

            # Validasi dalam segmen
            if not (0 <= s <= 1):
                continue

            intersections.append((i + 1, intersection))
            
            '''
            print(
                f"Titik potong pada segmen {i + 1}: "
                f"longitude = {intersection[0]:.6f}, "
                f"latitude = {intersection[1]:.6f}"
            )
            '''

        except np.linalg.LinAlgError:
            continue

    if not intersections:
        print("Tidak ditemukan titik potong")

    # ---------- PLOT ----------
    '''
    if plot:
        plt.figure(figsize=(9, 7))

        # Plot segmen
        for i in range(len(x) - 1):
            plt.plot(
                [x[i], x[i + 1]],
                [y[i], y[i + 1]],
                'k-', linewidth=2,
                label="Garis" if i == 0 else ""
            )

        # Plot vertex
        plt.scatter(x, y, c='k', s=40, zorder=3, label="Vertex")

        # Plot titik P
        plt.plot(P[0], P[1], 'go', markersize=9, label="Titik P")

        # Plot ray
        ray_end = P + 0.3 * v_theta
        plt.plot(
            [P[0], ray_end[0]],
            [P[1], ray_end[1]],
            'b--', linewidth=2,
            label=f"Arah θ = {theta_deg}°"
        )

        # Plot intersection points
        for idx, pt in intersections:
            plt.plot(
                pt[0], pt[1],
                'ro', markersize=8,
                label="Titik potong" if idx == intersections[0][0] else ""
            )

        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Deteksi Titik Potong Ray dengan Segmen Garis")
        plt.grid(True)
        plt.axis("equal")
        plt.legend()
        plt.show()
    '''
    return intersections



long_list = [105.992613, 105.989277, 105.966657,
     105.76885, 105.765563, 105.757095, 105.757006]

lat_list = [-5.924208, -5.924249, -5.918281,
     -5.868402, -5.868032, -5.86826, -5.86747]

P = [105.85, -5.95]
theta_deg = 90
while True:
    intersections = ray_segment_intersection_system(
        long_list, lat_list, P, theta_deg, plot=True
    )
    
    segment, coord = intersections[0]
    lat_cross, lon_cross = coord
    print(lat_cross, lon_cross)
    time.sleep(2)

