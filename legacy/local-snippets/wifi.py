import machine
import time
import network
import urequests

SSID = "Your-SSID-Here"
PASSWORD = "Your-Password-Here"
URL = "www.worldtimeapi.org/api/ip"

# station interface used to connect to existing WiFi signal
# api interface used to create new, connectable WiFi signal
def connectWifi():
    api_if = network.WLAN(network.AP_IF) # creates api interface
    api_if.active(False)
    sta_if = network.WLAN(network.STA_IF) # creates station interface
    if not sta_if.isconnected():
        print('Connecting to wifi...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Network config: ' + sta_if.ifconfig())


connectWifi() # calls the function

while True:
    response = urequests.get(URL)
    
