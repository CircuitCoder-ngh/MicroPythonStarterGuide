import machine
import time
import network
import urequests

SSID =
PASSWORD =
URL = "http://worldtimeapi.org/api/ip" # gets time based off your IP address

def connectWifi():
    api_if = network.WLAN(network.AP_IF)
    api_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to wifi...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Network config: ' + sta_if.ifconfig())

def getTime():
    try:
        response = urequests.get(URL)
        print(response.text) # returns string of all content
        # or
        text = response.json() # returns dictionary of content items
        print(text[__key__])
    except:
        print('Read data request failed')
        print(response.status_code) # 
        
