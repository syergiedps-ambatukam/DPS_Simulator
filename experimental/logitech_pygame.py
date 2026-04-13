import pygame
import time

pygame.init()
pygame.joystick.init()

js = pygame.joystick.Joystick(0)
js.init()

def dz(v, d=0.05):
    return 0 if abs(v) < d else v

while True:
    pygame.event.pump()

    roll  = dz(js.get_axis(0))
    pitch = dz(-js.get_axis(1))
    yaw   = dz(js.get_axis(2))
    thr   = (1 - js.get_axis(3)) / 2  # 0..1

    print(f"R:{roll:.2f} P:{pitch:.2f} Y:{yaw:.2f} T:{thr:.2f}")

    if js.get_button(0):
        print("TRIGGER")

    print("HAT:", js.get_hat(0))
    time.sleep(0.05)
