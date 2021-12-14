import machine
import time
import network
import urequests

MS_PIN =
URL = "https://maker.ifttt.com/trigger/motion_detected/with/key/dIDxWlD9J7wVt-dmweCbk1"

ms = machine.Pin(MS_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

msCounter = 0

# using the same debouncing process for buttons on the motion sensor
# allows for better control over how often the motion sensor
# can be triggered
def th(): 
    global msCounter
    if msCounter == 0:
        msCounter += 1

timer = machine.Timer(-1)
# period is in milliseconds, controls how often motion sensor can register
timer.init(period=100, mode=machine.Timer.PERIODIC, callback=th)

# connect ESP32 to Wi-Fi
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

# sends email to chosen address notifying that motion is detected
def motionDetected():
    try:
        urequests.get(URL)
        print('Data request successful')
    except:
        print('Data request failed')

connectWifi()
while True:
    if msCounter > 0:
        if ms.value() == 1:
            motionDetected()
