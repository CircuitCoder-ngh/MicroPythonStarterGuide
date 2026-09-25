# wifi.py - connect the ESP32 to your Wi-Fi network.
#
# Usage:
#   import wifi
#   wifi.connect()     # uses the SSID and PASSWORD from secrets.py

import time
import network


def connect(timeout_s=20):
    import secrets  # your Wi-Fi name and password live in secrets.py

    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to", secrets.SSID, "...")
        wlan.connect(secrets.SSID, secrets.PASSWORD)
        start = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), start) > timeout_s * 1000:
                raise RuntimeError("Could not connect to Wi-Fi. "
                                   "Check the name and password in secrets.py")
            time.sleep(0.25)
    print("Connected! IP address:", wlan.ipconfig("addr4")[0])
    return wlan
