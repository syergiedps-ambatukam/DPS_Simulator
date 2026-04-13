######  PROGRAM MEMANGGIL WINDOWS PYQT5 ##########################

####### memanggil library PyQt5 ##################################
#----------------------------------------------------------------#
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtQml import * 
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *  
import sys
import cvxpy as cp
from scipy.linalg import expm
import math
import pygame
import json
import time
import random
from scipy.optimize import linprog, minimize
import pandas as pd
data_saved_buffer = []
from datetime import datetime
import os
#----------------------------------------------------------------#

import numpy as np
from filterpy.kalman import KalmanFilter

def meter_conversion(coord1, coord1_alt, coord2, coord2_alt):
    return (coord2 - coord1) * 111000  # Faktor konversi kasar: 1 derajat ≈ 111.139 km

def meter_conversion_two_point(lat1, long1, lat2, long2):
    delta_lat = (lat1 - lat2)*111000
    delta_lon = (long1 - long2)*111000
    distance = sqrt(pow(delta_lat, 2) +  pow(delta_lon, 2))
    return distance

def ray_segment_intersection_system(x, y, P, theta_deg, plot=True):
    x = np.array(x)
    y = np.array(y)
    P = np.array(P)
    
    

    intersections = []

    theta_rad = np.radians(360-theta_deg)
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
            
            direction = "right"
            distance = meter_conversion_two_point(P[1], P[0], intersection[1], intersection[0])
            #intersections.append((i + 1, intersection))
            intersections.append({
                "segment": i + 1,
                "longitude": float(intersection[0]),
                "latitude": float(intersection[1]),
                "direction": direction,
                "distance" : distance
            })

        except np.linalg.LinAlgError:
            continue
        
    # ---------- HITUNG INTERSECTION ----------
    
    theta_rad = np.radians(360-theta_deg-180)
    v_theta = np.array([np.cos(theta_rad), np.sin(theta_rad)])
    for i in range(len(x) - 1):
        A = np.array([x[i], y[i]])
        B = np.array([x[i + 1], y[i + 1]])
        direction = ""

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
            
            direction = "left"
            distance = -meter_conversion_two_point(P[1], P[0], intersection[1], intersection[0])
            #intersections.append((i + 1, intersection))
            intersections.append({
                "segment": i + 1,
                "longitude": float(intersection[0]),
                "latitude": float(intersection[1]),
                "direction": direction,
                "distance" : distance
            })

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
        pass
        #print("Tidak ditemukan titik potong")
    
    # ---------- PLOT ----------
    return intersections



class PIDMIMO:
    def __init__(self, Kp, Ki, Kd, dt, u_min, u_max, Kaw=None):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt

        self.u_min = u_min.reshape((3,1))
        self.u_max = u_max.reshape((3,1))

        self.e_prev = np.zeros((3,1))
        self.e_int  = np.zeros((3,1))

        # Anti-windup gain (default = Ki)
        self.Kaw = Kaw if Kaw is not None else Ki

    def __call__(self, sp, pv):
        sp = sp.reshape((3,1))
        pv = pv.reshape((3,1))

        e = sp - pv
        e_dot = (e - self.e_prev) / self.dt

        # PID sebelum limit
        u_raw = (
            self.Kp @ e +
            self.Ki @ self.e_int +
            self.Kd @ e_dot
        )

        # Saturation
        u_sat = np.clip(u_raw, self.u_min, self.u_max)

        # Anti-windup (back-calculation)
        self.e_int += (e + self.Kaw @ (u_sat - u_raw)) * self.dt

        self.e_prev = e.copy()
        return u_sat

dt = 0.1

Kp = np.diag([0.1, 0.1, 1.5])
Ki = np.diag([0, 0, 0.0])
Kd = np.diag([0.5, 0.5, 0.3])

u_min = np.array([-10, -10, -8])   # Fx, Fy, Mz min
u_max = np.array([ 10,  10,  8])   # Fx, Fy, Mz max

pid = PIDMIMO(Kp, Ki, Kd, dt, u_min, u_max)




pubdelay = 2 #delay publish to all wind and engine box
counter = 0


start_lat = -5.924208
start_lon = 105.992613

latitude = -6.215861
latitude_dot = 0.00001
longitude = 107.803706
longitude_dot = 0.00001
yaw = -90


#rpl_lat = [-5.924208, -5.924249, -5.918281, -5.868402, -5.868032, -5.86826, -5.86747]
#[-5.924208]
#rpl_long = [105.992613, 105.989277, 105.966657, 105.76885, 105.765563, 105.757095, 105.757006]#[105.992613]


rpl_lat = [-5.924208,  -5.924051,  -5.924222,  -5.924041]
rpl_long = [105.992613,105.992493, 105.992120,105.991831]

rpl_lat_seg = [rpl_lat[0], rpl_lat[1]]
rpl_long_seg = [rpl_long[0], rpl_long[1]]

delta_lat = 0
delta_lon = 0
sp_lat = -6.215861
sp_lon = 107.803706
sp_yaw = 0

delta_x = 0.00001
delta_y = 0.0000
theta_dot = 1

x_dot = 0
y_dot = 0
eta = np.array([[x_dot], [y_dot], [yaw]])
V = np.array([[latitude_dot], [longitude_dot], [yaw]]) 

x_target = 0
y_target = 0


heading_error = 0

steering1 = 0
steering2 = 0
steering3 = 0
steering4 = 0

gas_throttle1 = 0
gas_throttle2 = 0
gas_throttle3 = 0
gas_throttle4 = 0
heading_error = 0

target_point = 1

lat_ytarget = 0
long_ytarget = 0

lat_xtarget = 0
long_xtarget = 0
y_direction = ""
y_distance = 0
x_direction = 0
x_distance = 0

theta_target = 0
theta_delta = 0

pid_mode = False



steering1_real = 0
steering2_real = 0
steering3_real = 0
steering4_real = 0

gas_throttle1_psuedo = 0
gas_throttle2_psuedo = 0
gas_throttle3_psuedo = 0
gas_throttle4_psuedo = 0


gas_throttle1_qp = 0
gas_throttle2_qp = 0
gas_throttle3_qp = 0
gas_throttle4_qp = 0



gas_throttle1_real = 0
gas_throttle2_real = 0
gas_throttle3_real = 0
gas_throttle4_real = 0

fx1_real = 0
fx2_real = 0
fx3_real = 0
fx4_real = 0



fy1_real = 0
fy2_real = 0
fy3_real = 0
fy4_real = 0


mz_real = 0

u_real = np.array([[0],[0],[0]])



#deg = list(range(0, 361, 10))
#val = [random.randint(0, 100) for _ in deg]

angles = np.arange(0, 361, 10)

deg = np.zeros(len(angles))
            
print(deg)
val = np.zeros(len(angles))

def coordinate_conv(x, y, theta):
    j_theta = np.array([[np.cos(theta * float(np.pi/180)), -np.sin(theta * float(np.pi/180)), 0],
              [np.sin(theta * float(np.pi/180)), np.cos(theta* float(np.pi/180)), 0],
              [0, 0, 1]])
    
    result = j_theta @ np.array([[x], [y], [0]])  # Gunakan 0 untuk rotasi biasa

    delta_lat = result[0, 0]  # Mengambil nilai skalar dari array
    delta_lon = result[1, 0]

    return delta_lat, delta_lon



def rotation(x, y, theta):
    j_theta = np.array([[np.cos(theta * float(np.pi/180)), -np.sin(theta * float(np.pi/180)), 0],
              [np.sin(theta * float(np.pi/180)), np.cos(theta* float(np.pi/180)), 0],
              [0, 0, 1]])
    
    result = j_theta @ np.array([[x], [y], [0]])  # Gunakan 0 untuk rotasi biasa

    x_accent = result[0, 0]  # Mengambil nilai skalar dari array
    y_accent = result[1, 0]
    theta = theta

    return x_accent, y_accent, theta



def shortest_psi(psi_ref, psi_d):
    psi_temp = (psi_ref-psi_d)%360
    psi_shortest = (psi_temp + 360) *-1 %360 
    if (psi_shortest > 180):
        psi_shortest = psi_shortest - 360
    return psi_shortest

import math

def map_angle_conversion(lat1, long1, lat2, long2):
    d_lat = (lat1 - lat2)*111000
    d_lon = (long1 - long2)*111000
    map_angle_conversion = math.atan2(float(d_lon),float(d_lat)) * (180/math.pi)
    return map_angle_conversion





def find_intersection_theta(A, B, P, theta_deg):
    theta_rad = np.radians(theta_deg)

    v_AB = np.array(B) - np.array(A)
    v_theta = np.array([np.cos(theta_rad), np.sin(theta_rad)])

    M = np.column_stack((v_AB, -v_theta))
    rhs = np.array(P) - np.array(A)

    if np.linalg.matrix_rank(M) < 2:
        # Parallel or identical lines
        return None

    try:
        sol = np.linalg.solve(M, rhs)
        s = sol[0]
        intersection = np.array(A) + s * v_AB

        # Validate that intersection is forward along the theta direction from P
        direction_vec = intersection - np.array(P)
        if np.dot(direction_vec, v_theta) < 0:
            # Intersection is behind the ray origin
            return None

        # Validate intersection lies within the segment AB
        if not (0 <= s <= 1):
            return None

        return intersection
    except np.linalg.LinAlgError:
        return None
    
from scipy.signal import lti, lsim
from scipy.optimize import lsq_linear
from math import sin, cos, sqrt, atan2, radians, atan
import paho.mqtt.client as paho

#Thruster allocation using QP
ly1 = 0.25
lx1 = 1

ly2 = -0.25
lx2 = 1

ly3 = -0.25
lx3 = -1

ly4 = 0.25
lx4 = -1

broker="127.0.0.1"
#broker="mqtt.ardumeka.com"
#broker = "broker.emqx.io"
#port = 11219
port = 1883
topic_test = ""

############ Model Kinetik ################################

print("==== Kinetik =======")
xg = 0 #posisi x center of gravity
yg = 0 #posisi y center of gravity
mass = 100 #massa kapal
r = 0 #posisi arah surge / kecepatan sudut (psi_dot)
Iz = 0 #momen inersia akibat percepatan sumbu y

x_u = 0.9
y_v = 0.6
n_r = 0.3
y_r = 0.1
n_v = 0.2

X_udot = 0.9
Y_vdot = 0.6
Y_rdot = 0.7
N_vdot = 0.3
N_rdot = 0.4
u = 0
v = 0
r = 0

j_theta = np.array([[0,0,0],[0,0,0],[0,0,0]])
v = np.array([[0],[0],[0]])
n_error = 0
e_error = 0
error_body_fixed = np.array([[0],[0],[0]])

x_error = 0
y_error = 0

yaw_sp = 0



#gaya akibat massa


#dari thesis teguh


M_RB = np.array([[(mass), 0 ,(-mass*yg)],
                 [0, (mass) ,(mass*xg)],
                 [(-mass*yg), (mass*xg) ,(Iz)]])

M_AM = np.array([[(-X_udot), 0 ,(0)],
                 [0, (-Y_vdot) ,(-Y_rdot)],
                 [(0), (-N_vdot) ,(N_rdot)]])



#m = M_RB + M_AM
m = np.array([[120, 0, 0],[0, 120, 0],[0, 0, 120]])

print("m",m)
'''
#dari Thomas P. DeRensis
m = np.array([[mass, -0, 0], [0.0, mass, mass*xg], [-0.00, mass*xg, Iz]])
+ np.array([[-X_udot,-0.00,0.00],[-0.00,Y_vdot,Y_rdot],[-0.00,N_vdot,n_rdot]])
print(m)
'''


#gaya akibat coriolis
c = np.array([ [0, 0, -mass * (xg*r + float(y_dot))],
               [0, 0, -mass * (yg*r + float(x_dot))],
               [-mass * (xg*r + float(y_dot)),-mass * (yg*r + float(x_dot)), 0]]) + np.array([[0,0,-Y_vdot*float(y_dot) - ((Y_rdot+N_vdot)/2)*r],
            [0,0,X_udot*float(x_dot)],
            [-Y_vdot*float(y_dot) - ((Y_rdot+N_vdot)/2)*r,X_udot*float(x_dot),0]])

#gaya akibat drag

'''
d = np.array([[x_u,-0.00,-0.00],
    [-0.00,y_v,y_r],
    [-0.00,n_v,n_r]]) 
'''

d = np.diag([40.0, 50.0, 20.0]) 
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

x_next = np.array([[0], [0], [0], [0], [0], [0]])
 

x = np.array([[0], [0], [0], [0], [0], [0]]) 
u_optimal = np.array([[0], [0], [0]])
y = np.array([[0], [0.0], [0]])

np.set_printoptions(formatter={'float': '{:0.3f}'.format})

print("Continous state space : ")
print("A")
print(str(A))

print("B")
print(B)

print("C")
print(C)


print("D")
print(D)

# Mendiskretisasi matriks A dan B
# Matriks identitas
I = np.eye(A.shape[0])
T = 1

# Menghitung Ad dan Bd dengan Tustin
Ad = np.linalg.inv(I - (T/2) * A) @ (I + (T/2) * A)
Bd = np.linalg.inv(I - (T/2) * A) @ (T * B)

# Cd dan Dd tetap sama
Cd = C
Dd = D


print("Discrete state space : ")
print("A")
print(str(Ad))

print("B")
print(Bd)

print("C")
print(Cd)


print("D")
print(Dd)





# Matriks T untuk 4 baling-baling
T = np.array([[1, 0, 1, 0, 1, 0, 1, 0],   # Menambah kolom untuk F_x4
              [0, 1, 0, 1, 0, 1, 0, 1],   # Menambah kolom untuk F_y4
              [-ly1, lx1, -ly2, lx2, -ly3, lx3, -ly4, lx4]])  # Menyesuaikan gaya kontrol

T_transpose = T.T
W = np.eye(8)
W_inv = np.linalg.inv(W)
TWT_inv = np.linalg.inv(T @ W_inv @ T_transpose)
T_pseudo_inverse = W_inv @ T_transpose @ TWT_inv
tau_control = np.array([0, 0, 10])


T_nonlinear = np.array([
    [np.cos(np.deg2rad(steering1)), np.cos(np.deg2rad(steering2)), np.cos(np.deg2rad(steering3)), np.cos(np.deg2rad(steering4))],         # Fx
    [np.sin(np.deg2rad(steering1)), np.sin(np.deg2rad(steering2)), np.sin(np.deg2rad(steering3)), np.sin(np.deg2rad(steering4))],         # Fy
    # Ganti baris Mz di T_nonlinear menjadi:
    [
        ((lx1 * np.sin(np.deg2rad(steering1))) - (ly1 * np.cos(np.deg2rad(steering1)))),
        ((lx2 * np.sin(np.deg2rad(steering2))) - (ly2 * np.cos(np.deg2rad(steering2)))),
        ((lx3 * np.sin(np.deg2rad(steering3))) - (ly3 * np.cos(np.deg2rad(steering3)))),
        ((lx4 * np.sin(np.deg2rad(steering4))) - (ly4 * np.cos(np.deg2rad(steering4))))
    ]   # Mz
])


tau_x = 0
tau_y = 0
M_z = 0



# ===== Parameter MPC =====
N = 10  # Prediction horizon
#Q =  10000
Q = np.diag([10000, 10000, 10000])  # Penalty for output error (adjusted for 3 outputs)
R = np.diag([1, 1, 1])  # Penalty for control effort (adjusted for 3 inputs)
delta_u_penalty = np.diag([10, 10, 10])  # Penalti perubahan kontrol (adjusted for 3 inputs)
u_min, u_max = -2, 2  # Batas kontrol

# ===== Variabel Simulasi =====
x0 = np.array([[0], [0], [yaw], [0], [0], [0]])   # Status awal
print("x0 =", x0)
predicted_states = []
applied_inputs = []
time_steps = []
y = np.array([[0], [0.0], [0]])
y_ref = np.array([0, 0, 10]).reshape(-1, 1)

heading_error = 0

# VARIABEL KALMAN FILTER
dim_x = 6  
dim_z = 3

kf = KalmanFilter(dim_x=dim_x, dim_z=dim_z)

kf.F = A
kf.B = B
kf.H = C

kf.Q = np.eye(dim_x) * 1e-4  # Noise proses
kf.R = np.diag([0.1, 0.1, 0.1])  # Noise pengukuran
kf.P = np.eye(dim_x) * 1.0  # Kovariansi awal

kf.x = x

joystick_state = False

intersect_detect = False

pv_x = 0
pv_y = 0
pv_theta = 0

publish_time = 0
publish_time_prev = 0

print("kalman filter succesfully defined ... ")

thruster_allocation_method = 0

filename = "recording.csv"


def save_to_custom_csv(lat, long, target_tau, actual_tau,thruster_allocation_method, filename):
    data = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
        'lat': lat,
        'long': long,
        'fx': target_tau[0].item(),
        'fy': target_tau[1].item(),
        'mz': target_tau[2].item(),
        'fx_actual': actual_tau[0].item(),
        'fy_actual': actual_tau[1].item(),
        'mz_actual': actual_tau[2].item(),
        'thruster allocation': thruster_allocation_method
    }
    
    df = pd.DataFrame([data])
    
    # Cek apakah file sudah ada
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)



class Worker(QThread):
    
    state_updated = pyqtSignal(float, float, float)  # x, y, yaw

    def __init__(self):
        super().__init__()
        self.running = True
        global joystick_state
        # ========= INIT PYGAME =========
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("❌ Joystick tidak terdeteksi")
            self.js = None
        else:
            self.js = pygame.joystick.Joystick(0)
            self.js.init()
            joystick_state = True
            print("✅ Joystick terdeteksi:", self.js.get_name(), joystick_state)
            

    def deadzone(self, val, dz=0.05):
        return 0.0 if abs(val) < dz else val

    def run(self):
        
        while self.running:
            #print("dari worker", latitude)
            
            global latitude
            global latitude_dot
            global longitude
            global longitude_dot
            global yaw
            global yaw_dot
            global V
            global x
            global x0
            global x_next
            global y
            global y_ref
            
            global steering1
            global steering2
            global steering3
            global steering4
            
            global gas_throttle1
            global gas_throttle2
            global gas_throttle3
            global gas_throttle4
            global x0
            global U
            global heading_error
            global u_optimal
            
            global n_error
            
            global latitude_now 
            global longitude_now
            
            global x_target
            global y_target
            
            global start_lat
            global start_lon
            
            global delta_lat
            global delta_lon
            
            
            global lat_ytarget
            global long_ytarget
            global intersect_detect
            
            global target_point
            
            global x_distance
            global x_direction
            
            global y_direction
            global y_distance
            
            global lat_xtarget
            global long_xtarget
            
            global pv_x
            global pv_y
            global pv_theta
            
            global theta_target
            global theta_delta
            global joystick_state

            global publish_time_prev
            global publish_time
            
            global rpl_lat_seg
            global rpl_long_seg
            
            global steering1_real, steering2_real, steering3_real, steering4_real
            global gas_throttle1_real, gas_throttle2_real, gas_throttle3_real, gas_throttle4_real
            global gas_throttle1_psuedo, gas_throttle2_psuedo,gas_throttle3_psuedo, gas_throttle4_psuedo
            global gas_throttle1_qp, gas_throttle2_qp, gas_throttle3_qp, gas_throttle4_qp
            global fx1_real, fx2_real,fx3_real,fx4_real, fy1_real, fy2_real,fy3_real, fy4_real,mz_real
            global u_real
            
            global deg
            global val
            
            global thruster_allocation_method
            
            
            steering_array = np.array([steering1_real, steering2_real, steering3_real, steering4_real])
            Fmax = np.array([10, 10, 10, 10])

            theta = np.deg2rad(steering_array)
            angles = np.arange(0, 361, 10)

            #deg = np.zeros(len(angles))
            
            #print(deg)
            #val = np.zeros(len(angles))
            
            
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
                    
                    #print(f"{phi_deg:3d} | " f"{F[0]:5.2f} {F[1]:5.2f} {F[2]:5.2f} {F[3]:5.2f} | "f"{F_total:6.2f}")
                    
                else:
                    #print(f"{phi_deg:3d} | No solution")
                    F_total = 0

                deg[k] = int(phi_deg)
                val[k] = int(F_total)
            
            
            
            
            #print(deg)
            #print(steering1_real, steering2_real, steering3_real, steering4_real)
            
            
            
            # ===== UPDATE JOYSTICK =====
            pygame.event.pump()

            if self.js:
                roll  = self.deadzone(self.js.get_axis(0))   # sway
                pitch = self.deadzone(-self.js.get_axis(1))  # surge
                yaw_j = self.deadzone(self.js.get_axis(2))   # yaw
                thr   = (1 - self.js.get_axis(3)) / 2         # throttle 0..1
                #print(roll)

                # ===== SCALING =====
                tau_x_joystick = pitch  * 2.0    # surge force
                tau_y_joystick = roll  * 2.0   # sway force
                M_z_joystick   = yaw_j * 1.0         # yaw moment
                
               
            P = [longitude, latitude]
             
            
            intersections = ray_segment_intersection_system(
                #rpl_long, rpl_lat, P, yaw, plot=True
                rpl_long_seg, rpl_lat_seg, P, yaw, plot=True
            )

            if intersections:
                first = intersections[0]

                segment     = first["segment"]
                long_ytarget= first["longitude"]
                lat_ytarget = first["latitude"]
                y_direction = first["direction"]
                y_distance  = first["distance"]

                intersect_detect = True
            else:
                intersect_detect = False

            
            #print(y_direction, y_distance, "|", x_distance,"target_point", target_point, len(rpl_long))
            
         
            lat_xtarget = rpl_lat[target_point]
            long_xtarget = rpl_long[target_point]
            try:
                x_distance = meter_conversion_two_point(latitude, longitude, rpl_lat[target_point], rpl_long[target_point])
                if ((x_distance < 10) and (target_point < (len(rpl_lat) -1))):
                    target_point = target_point + 1
            except:
                pass
            
            theta_target = map_angle_conversion(rpl_lat[target_point], rpl_long[target_point], latitude, longitude)
            
                
            #print(joystick_state)
            if (joystick_state == True):
                u_optimal = np.array([[tau_x_joystick],[tau_y_joystick],[M_z_joystick]])
            
            else :
                if (pid_mode ==  True):
                    sp = np.array([0, 0, 0])     # target
                    print("x_dist : ", x_distance,"y_dist : ", y_distance, "theta_delta", theta_delta)
                    theta_delta = shortest_psi(theta_target, yaw)
                    if (abs(theta_delta) >= 10 and (x_distance > 15)):
                        
                        pv_x = 0
                        pv_y = 0
                        pv_theta = theta_delta

                    else:
                        
                        if (target_point < int(len(rpl_lat) -1)) and (x_distance > 15):
                            pv_theta = theta_delta
        
                            pv_x = -x_distance
                            pv_y = -y_distance
                            #print("a")
                        else:
                            pv_theta = 0
                            if (theta_delta > 0 and theta_delta < 90):
                                pv_x = -x_distance
                                pv_y = -y_distance
                                print("a")
                                
                                
                            if (theta_delta > 90 and theta_delta < 180):
                                pv_x = x_distance
                                pv_y = -y_distance
                                print("b")
                                
                            
                            if (theta_delta > -90 and theta_delta < 0):
                                pv_x = -x_distance
                                pv_y = y_distance
                                print("c")
                                
                                
                            if (theta_delta > -180 and theta_delta < -90):
                                pv_x = x_distance
                                pv_y = y_distance
                                print("d")
                                
                                
                            #print("b")

                    pv = np.array([pv_x, pv_y, pv_theta])     # feedback
                    
                    u_optimal = pid(sp, pv)
                    
                    #print(theta_delta, theta_target, yaw)
                    rpl_lat_seg = [rpl_lat[target_point -1], rpl_lat[target_point]]
                    rpl_long_seg = [rpl_long[target_point - 1], rpl_long[target_point]]

                    #print(x_distance, pv_y, pv_theta, "|", theta_delta, "|", target_point, (len(rpl_lat) -1))
                else:
                    u_optimal = np.array([[tau_x],[tau_y],[M_z]])
            
            
            
            
                
            # ===== Simulasikan Sistem =====
            print(u_real)
            x0 = Ad @ x0 + Bd @ u_real.reshape(-1, 1)
            #x0 = A @ x0 + B @ np.array([[0.0001], [0], [0]])
            y = Cd @ x0
            #print(x0)

            #Kalman filter
            kf.predict(u= u_optimal.reshape(-1, 1))  # Prediksi dengan sinyal kendali
            kf.update(y)  # Update dengan data sensor
            #print(f"Estimasi theta: {kf.x[0, 0]:.2f}, omega: {kf.x[1, 0]:.2f}")

            # Simpan Hasil
            predicted_states.append(y.flatten())
            applied_inputs.append(u_optimal)
            
            
            delta_x = y[0][0]
            delta_y = y[1][0]
            
            delta_lat, delta_lon = coordinate_conv(delta_x, delta_y, yaw) 
            #print(f"d_lat : {delta_lat}, d_lon: {delta_lon}")
            
            latitude = start_lat + (delta_lat/111000)
            longitude = start_lon + (delta_lon/111000)
            yaw = y[2][0]
            
            tau_control = u_optimal
            #Steering Dynamics
            if (steering1<0):
                steering1 = 360 + steering1
                
            if (steering2<0):
                steering2 = 360 + steering2
                
            if (steering3<0):
                steering3 = 360 + steering3
                
            if (steering4<0):
                steering4 = 360 + steering4
            
            #print(shortest_psi(steering1, steering1_real)) untuk steering dps real
            if (shortest_psi(steering1, steering1_real)) > 0:
                steering1_real -=1
            if (shortest_psi(steering1, steering1_real)) < 0:
                steering1_real +=1
                
            if (shortest_psi(steering2, steering2_real)) > 0:
                steering2_real -=1
            if (shortest_psi(steering2, steering2_real)) < 0:
                steering2_real +=1
                
            if (shortest_psi(steering3, steering3_real)) > 0:
                steering3_real -=1
            if (shortest_psi(steering3, steering3_real)) < 0:
                steering3_real +=1
            
            if (shortest_psi(steering4, steering4_real)) > 0:
                steering4_real -=1
            if (shortest_psi(steering4, steering4_real)) < 0:
                steering4_real +=1
                
            
            steering1_real %= 360
            steering2_real %= 360
            steering3_real %= 360
            steering4_real %= 360
            
            
            # Gaya yang harus diberikan oleh setiap thruster Metode 1 dan 2
            
            if (thruster_allocation_method == 0 or thruster_allocation_method == 1):
                f = T_pseudo_inverse @ tau_control

                '''
                              ^
                    #####################
                    #==4==         ==1==#
                    #                   #
                    #                   #
                    #                   # -----------> Thruster Orientation
                    #         x         #
                    #                   #
                    #                   #
                    #==3==         ==2==#
                    #####################
                '''

                try:
                    steering1 = math.atan2(float(f[1]),float(f[0])) * 180/math.pi
                except:
                    steering1 = 90

                try:
                    steering2= math.atan2(float(f[3]),float(f[2])) * 180/math.pi
                except:
                    steering2 = 90

                try:
                    steering3 = math.atan2(float(f[5]),float(f[4])) * 180/math.pi
                except:
                    steering3 = 90

                try:
                    steering4 = math.atan2(float(f[7]),float(f[6])) * 180/math.pi
                except:
                    steering4 = 90
                
            
                gas_throttle1_psuedo = math.sqrt(float(f[1])**2 + float(f[0])**2)
                gas_throttle2_psuedo = math.sqrt(float(f[3])**2 + float(f[2])**2)
                gas_throttle3_psuedo = math.sqrt(float(f[5])**2 + float(f[4])**2)
                gas_throttle4_psuedo = math.sqrt(float(f[7])**2 + float(f[6])**2)
                
                #metode 1 angka yang diberikan langsung dikirim ke thruster 
            if (thruster_allocation_method == 0):
                gas_throttle1 = gas_throttle1_psuedo
                gas_throttle2 = gas_throttle2_psuedo
                gas_throttle3 = gas_throttle3_psuedo
                gas_throttle4 = gas_throttle4_psuedo
                
            
            
            
            #metode 2 nilai thrust disesuaikan dengan Linear Programming berdasarkan posisi azimuth thruster sebelum dikirim
            if (thruster_allocation_method == 1):
               
                #print(steering1_real, steering2_real, steering3_real, steering4_real)
                
                
                tau_dummy = tau_control
                T_nonlinear = np.array([
                        [np.cos(np.deg2rad(steering1_real)), np.cos(np.deg2rad(steering2_real)), np.cos(np.deg2rad(steering3_real)), np.cos(np.deg2rad(steering4_real))],         # Fx
                        [np.sin(np.deg2rad(steering1_real)), np.sin(np.deg2rad(steering2_real)), np.sin(np.deg2rad(steering3_real)), np.sin(np.deg2rad(steering4_real))],         # Fy
                        # Ganti baris Mz di T_nonlinear menjadi:
                        [
                            ((lx1 * np.sin(np.deg2rad(steering1_real))) - (ly1 * np.cos(np.deg2rad(steering1_real)))),
                            ((lx2 * np.sin(np.deg2rad(steering2_real))) - (ly2 * np.cos(np.deg2rad(steering2_real)))),
                            ((lx3 * np.sin(np.deg2rad(steering3_real))) - (ly3 * np.cos(np.deg2rad(steering3_real)))),
                            ((lx4 * np.sin(np.deg2rad(steering4_real))) - (ly4 * np.cos(np.deg2rad(steering4_real))))
                        ]   # Mz
                    ])
                print(T_nonlinear)
                tau_dummy = tau_control.flatten()
                def objective(x):
                    error = np.dot(T_nonlinear, x) - tau_dummy
                    
                    return np.sum(error**2) # Least squares error
                
                bounds = [(0, 5) for _ in range(4)]
                x_guess = np.array([0, 0, 0, 0])
                res = minimize(objective, x_guess, bounds=bounds, method='L-BFGS-B')
                if res.success:
                    F = res.x
                    
                    gas_throttle1 = F[0]
                    gas_throttle2 = F[1]
                    gas_throttle3 = F[2]
                    gas_throttle4 = F[3]
                    actual_b = np.dot(T_nonlinear, F)
                    #print("\nTarget vs Hasil Nyata:")
                    #print(f"Fx: Target {tau_dummy[0]} -> Hasil {actual_b[0]:.3f}")
                    #print(f"Fy: Target {tau_dummy[1]} -> Hasil {actual_b[1]:.3f}")
                    #print(f"Mz: Target {tau_dummy[2]} -> Hasil {actual_b[2]:.3f}")
                    
                    



            
            
            gas_throttle1_real = (1 * gas_throttle1)
            gas_throttle2_real = (1 * gas_throttle2)
            gas_throttle3_real =(1 * gas_throttle3)
            gas_throttle4_real = (1 * gas_throttle4)

            #F real + noise
            fx1_real = gas_throttle1_real * math.cos(steering1_real * math.pi/180)
            fx2_real = gas_throttle2_real * math.cos(steering2_real * math.pi/180)
            fx3_real = gas_throttle3_real * math.cos(steering3_real * math.pi/180)
            fx4_real = gas_throttle4_real * math.cos(steering4_real * math.pi/180)
            
            fy1_real = gas_throttle1_real * math.sin(steering1_real * math.pi/180)
            fy2_real = gas_throttle2_real * math.sin(steering2_real * math.pi/180)
            fy3_real = gas_throttle3_real * math.sin(steering3_real * math.pi/180)
            fy4_real = gas_throttle4_real * math.sin(steering4_real * math.pi/180)
            
            
            f_real = np.array([
                fx1_real, fy1_real,
                fx2_real, fy2_real,
                fx3_real, fy3_real,
                fx4_real, fy4_real
            ]).reshape(8, 1)

            u_real = T @ f_real   # ← FINAL & BENAR
            
            
            #print(fy1_real, fy2_real,fy3_real,fy4_real)
            '''
            print("--------------")
            print(f, "|", u_optimal)
            print("              ")
            print(f_real, "|", u_real)
            print("--------------")
            '''
            publish_time = time.time() - publish_time_prev
            if (publish_time > 0.2):
                
                if(pid_mode == True):
                    save_to_custom_csv(latitude, longitude, u_optimal, u_real,thruster_allocation_method, filename)
                
                
                
                
                #print("tick")
                client.publish("propeller1",str(gas_throttle1 *10))
                #client.publish("propeller2",str(gas_throttle2*10))
                #client.publish("propeller3",str(gas_throttle3*10))
                client.publish("propeller4",str(gas_throttle4*10))

                if (steering1_real > 0):
                    client.publish("steering1",str(int(steering1_real)))
                else:
                    client.publish("steering1",str(int(359 + steering1_real)))
                
                if (steering2_real > 0):
                    client.publish("steering2",str(int(steering2_real)))
                else:
                    client.publish("steering2",str(int(359 + steering2_real)))

                if(steering3_real > 0):
                    client.publish("steering3",str(int(steering3_real)))
                else:
                    client.publish("steering3",str(int(359 + steering3_real)))
                
                if (steering4_real > 0):
                    client.publish("steering4",str(int(steering4_real)))
                else:
                    client.publish("steering4",str(int(359 + steering4_real)))
                publish_time_prev = time.time()
                
            
            
            
            
            self.msleep(200)

########## mengisi class table dengan instruksi pyqt5#############
#----------------------------------------------------------------#
class table(QObject):    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty("backend", self)    
        self.engine.load(QUrl("main.qml"))
        
        # Jalankan worker thread
        self.worker = Worker()
        self.worker.state_updated.connect(self.update_state)
        self.worker.start()
        
        self.lat_send = latitude
        self.long_send = longitude
        
        
        sys.exit(self.app.exec_())
    
    @pyqtSlot(float, float, float)
    def update_state(self, latitude, y, yaw):
        pass
        #print(f"State: x={x:.2f}, y={y:.2f}, yaw={yaw:.2f}")
        
    @pyqtSlot(result=float)
    def latitude(self):return round(latitude,7)
    
    @pyqtSlot(result=float)
    def longitude(self):return round(longitude,7)
    
    @pyqtSlot(result=bool)
    def intersect_detect(self):return round(intersect_detect)
    
    
    @pyqtSlot(result=float)
    def lat_ytarget(self):return round(lat_ytarget,7)
    
    @pyqtSlot(result=float)
    def long_ytarget(self):return round(long_ytarget,7)
    

    @pyqtSlot(result=float)
    def lat_xtarget(self):return round(lat_xtarget,7)
    
    @pyqtSlot(result=float)
    def long_xtarget(self):return round(long_xtarget,7)
    


    
    @pyqtSlot(result=float)
    def start_lat(self):return round(start_lat,7)
    
    @pyqtSlot(result=float)
    def start_lon(self):return round(start_lon,7)
    
    
    @pyqtSlot(result=float)
    def delta_lat(self):return round(delta_lat)
    
    @pyqtSlot(result=float)
    def delta_lon(self):return round(delta_lon)
    
    
    
    @pyqtSlot(result=float)
    def steering1(self):return round(steering1)
    
    @pyqtSlot(result=float)
    def steering2(self):return round(steering2)
    
    @pyqtSlot(result=float)
    def steering3(self):return round(steering3)
    
    @pyqtSlot(result=float)
    def steering4(self):return round(steering4)
    
    
    @pyqtSlot(result=float)
    def steering1_real(self):return round(steering1_real)
    
    @pyqtSlot(result=float)
    def steering2_real(self):return round(steering2_real)
    
    @pyqtSlot(result=float)
    def steering3_real(self):return round(steering3_real)
    
    @pyqtSlot(result=float)
    def steering4_real(self):return round(steering4_real)
    
    
    
    @pyqtSlot(result=float)
    def lat_dest(self):return float((rpl_lat[0]))
    
    @pyqtSlot(result=float)
    def lon_dest(self):return float((rpl_long[0]))
    

    @pyqtSlot(result = float)
    def yaw_sp(self):return yaw_sp

    @pyqtSlot(result=float)
    def gas_throttle1(self):return round(gas_throttle1,3)
    
    @pyqtSlot(result=float)
    def gas_throttle2(self):return round(gas_throttle2,3)
    
    @pyqtSlot(result=float)
    def gas_throttle3(self):return round(gas_throttle3,3)
    
    @pyqtSlot(result=float)
    def gas_throttle4(self):return round(gas_throttle4,3)
    
    
    @pyqtSlot(result=float)
    def gas_throttle1_real(self):return round(gas_throttle1_real,3)
    
    @pyqtSlot(result=float)
    def gas_throttle2_real(self):return round(gas_throttle2_real,3)
    
    @pyqtSlot(result=float)
    def gas_throttle3_real(self):return round(gas_throttle3_real,3)
    
    @pyqtSlot(result=float)
    def gas_throttle4_real(self):return round(gas_throttle4_real,3)
    
    @pyqtSlot(int)
    def thruster_allocation_method (self, msg):
        global thruster_allocation_method
        thruster_allocation_method = msg
        print(thruster_allocation_method)
    
    @pyqtSlot(str)
    def pop(self, msg):
        global rpl_lat
        global rpl_long
        global yaw_sp
        if (len(rpl_lat) > 1):
            rpl_lat = rpl_lat[1:]
            rpl_long = rpl_long[1:]
        
        print(rpl_lat)
        print(rpl_long)
        
        yaw_sp = map_angle_conversion(float(rpl_lat[0]), float(rpl_long[0]),float(latitude), float(longitude))
    
    
    @pyqtSlot(result=list)
    def deg(self):
        return deg.tolist()

    @pyqtSlot(result=list)
    def val(self):
        return val.tolist()
    
    
    @pyqtSlot(str)
    def filename(self, msg):
        global filename
        filename = msg
        print(filename)
        
        
    @pyqtSlot(int)
    def tick(self, tick):
        pass
        '''
        
        
        first = random.random()*150
        val = [random.randint(0, 100) for _ in deg]
        val[-1] = val[0]
        
        
        print(deg)
        print(val)
        '''
        
    
    @pyqtSlot(str, str, str)
    def setpoint(self, message1, message2, message3):
        global sp_lat
        global sp_lon
        global sp_yaw
        global y_ref
        global latitude
        global longitude
        
        global start_lat
        global start_lon
        
        global delta_lat
        global delta_lon
        global yaw
        global y
        global x0
        global heading_error
        
        global yaw_sp
        
        
        
        delta_lat = 0
        delta_lon = 0
        
        sp_lat = float(message1)
        sp_lon = float(message2)
        sp_yaw = float(message3)
        
        start_lat = latitude
        start_lon = longitude
        
               
        
        
        j_theta = np.array([[np.cos(yaw * float(np.pi/180)), -np.sin(yaw * float(np.pi/180)), 0],
              [np.sin(yaw * float(np.pi/180)), np.cos(yaw* float(np.pi/180)), 0],
              [0, 0, 1]])
                
        try:
            n_error = round(meter_conversion(latitude, 0, float(sp_lat), 0))
            e_error = round(meter_conversion(longitude, 0, float(sp_lon), 0))
        except:
            n_error = 0
            e_error = 0
            

        #error_body_fixed = np.linalg.inv(j_theta) @ np.array([[n_error],[e_error],[yaw]])
        error_body_fixed = j_theta.T @ np.array([[n_error], [e_error], [yaw]])  # Gunakan .T

        x_error = (round(float(error_body_fixed[0]),1))
        y_error = (round(float(error_body_fixed[1]),1))
        
        
        x0[0:2] = 0
        #print()
        
        #heading_error = shortest_psi(heading, heading_target)
        y_ref = np.array([x_error, y_error, sp_yaw]).reshape(-1, 1)
        
        
        
        #print(start_lat, start_lon, sp_yaw)
    
    
    @pyqtSlot(str)
    def animate(self, message):
        pass
        
        
    
    @pyqtSlot(result=float)
    def yaw(self):return yaw
    
    @pyqtSlot(result=str)
    def A_ss(self):return str(np.round(Ad, decimals=4))
    
    @pyqtSlot(result=str)
    def B_ss(self):return str(Bd)
    
    @pyqtSlot(result=str)
    def C_ss(self):return str(Cd)
    
    @pyqtSlot(result=str)
    def x_ss(self):return str(np.round(x0, decimals=2))
    
    @pyqtSlot(result='QVariantList')
    def x_list(self):
        return np.round(x0.flatten(), 2).tolist()

    
    @pyqtSlot(result=str)
    def u_ss(self):return str(np.round(u_optimal.reshape(-1, 1), decimals=4))
    
    @pyqtSlot(result=str)
    def y_ss(self):return str(np.round(y, decimals=3))
    
    
    @pyqtSlot(result=str)
    def ureal_ss(self):return str(np.round(u_real, decimals=3))
    
    
    @pyqtSlot(result=str)
    def yref_ss(self):return str(np.round(y_ref, decimals=3))
    
    
    @pyqtSlot(result=list)
    def rpl_lat(self):return rpl_lat


    @pyqtSlot(result=list)
    def rpl_long(self):return rpl_long
    
    @pyqtSlot(float, float, float)
    def force(self, fx, fy, fz):
        global tau
        global tau_x
        global tau_y
        global M_z
        
        tau_x = fx
        tau_y = fy
        M_z = fz
    
    
    @pyqtSlot(result=int)
    def get_tiempo(self):
        date_time = QDateTime.currentDateTime()
        unixTIME = date_time.toSecsSinceEpoch()
        #unixTIMEx = date_time.currentMSecsSinceEpoch()
        return unixTIME
    
    @pyqtSlot(str, str)
    def kp(self, value1, value2):
        """
        value1 : JSON string matrix 3x3
        value2 : label / identifier (opsional)
        """

        # Parse JSON → Python list
        matrix_list = json.loads(value1)

        # Convert ke numpy array
        Kp = np.array(matrix_list, dtype=float)
        '''
        print("Received:", value2)
        print("Kp numpy array:")
        print(Kp)
        print("Shape:", Kp.shape)
        '''
    
    @pyqtSlot('QString', 'QString')
    def rpl_point(self, value1, value2):
        global rpl_lat
        global rpl_long
        global heading_target

        rpl_lat.append(str(round(float(value1), 6)))
        rpl_long.append(str(round(float(value2), 6)))
        print(rpl_lat)
        print(rpl_long)
        
        '''
        if (heading_first == "yes"):
            try:
                heading_target = int(shortest_psi(heading, map_angle_conversion(float(rpl_lat[0]), float(rpl_long[0]), val_latitude, val_longitude)))
                
            except:
                heading_target = 0

            print(f"heading target = {heading_target}")
        '''
    @pyqtSlot('bool')
    def pid_mode(self, val):
        global pid_mode    
        pid_mode = val
        print(pid_mode)
    
    
    
#----------------------------------------------------------------#


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    t = str(message.topic)

    if(msg[0] == 'c'):
        val =  1
    else:
        val = (msg)
    
    if (t == "slider_husni"):
        global topic_test
        topic_test = (msg)
        print(topic_test)
        

########## memanggil class table di mainloop######################
#----------------------------------------------------------------#    
if __name__ == "__main__":
    
    client= paho.Client("PC_1")
    client.on_message=on_message

    print("connecting to broker ",broker)
    client.connect(broker,port)#connect
    print(broker," connected")
    
    client.loop_start()
    print("Subscribing")

    client.subscribe("slider_husni")

    main = table()
    
    
#----------------------------------------------------------------#
    
