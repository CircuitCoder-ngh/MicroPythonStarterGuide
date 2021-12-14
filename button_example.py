import machine
import time

buttonCounter = 0

BUTTON_PIN = 14
LED_PIN = 27

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(LED_PIN, machine.Pin.OUT)

def th(timer): 
    global buttonCounter
    if buttonCounter == 0:
        buttonCounter += 1

timer = machine.Timer(-1) 
timer.init(period=200, mode=machine.Timer.PERIODIC, callback=th)

# use led.value() to check whether the LED is on or off,
# if it is off then the value returned will be 0,
# if it is on then the value returned will be 1

def change_led():
    if led.value() == 0:
        led.on()
    else:
        led.off()

while True:
    if buttonCounter > 0:
        if button.value() == 0:
            buttonCounter -= 1
            change_led()

