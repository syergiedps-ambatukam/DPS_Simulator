import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

time.sleep(1)  # beri waktu modul siap

nets = wlan.scan()


while True:
    nets = wlan.scan()
    print("SSID | RSSI (dBm) | Channel | Security")
    for net in nets:
        ssid = net[0].decode()
        bssid = net[1]
        channel = net[2]
        rssi = net[3]
        security = net[4]
        hidden = net[5]
        print(f"{ssid:20} {rssi:5} {channel:7} {security}")
    time.sleep(2)