# Connect to Wi-Fi (needs wifi.py and your secrets.py on the board)
import wifi

wlan = wifi.connect()
print("Signal strength:", wlan.status("rssi"), "dBm")
