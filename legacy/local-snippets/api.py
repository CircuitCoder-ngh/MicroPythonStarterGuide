import machine
import time
import network
import urequests

SSID = "Your-SSID-Here"
PASSWORD = "Your-Password-Here"
URL = "www.worldtimeapi.org/api/ip"

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
    print('Network config: ' + str(sta_if.ifconfig()))


connectWifi() 

# when we get data it usually comes in json format, therefore we use
# the .json() function to convert the data into something readable, usually
# in the form of a dictionary data type
while True:
# updates and prints time every second
    response = urequests.get(URL) # gets raw data
    text = response.json() # converts data into readable dictionary format
    datetime = text["datetime"] # isolates datetime from the rest of data
    date = datetime[0:10] # isolates date from datetime string
    localtime = datetime[11:19] # isolates time from datetime string
    # datetime[11:16] returns time without seconds

    print(localtime)
    time.sleep(1)
