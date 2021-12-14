import machine
import time

# abbreviating 'motion sensor' to 'ms'
MS_PIN = 36 # any pin that can work as input with a pull-up resistor
LED_PIN = 14

ms = machine.Pin(MS_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(LED_PIN, machine.Pin.OUT)

msCounter = 0 # global variables must be defined before used in a function

# using the same debouncing process for buttons, on the motion sensor,
# allows for better control over how often the motion sensor
# can be triggered
def th(): 
    global msCounter
    if msCounter == 0:
        msCounter += 1

timer = machine.Timer(-1)
# period is in milliseconds, controls how often motion sensor can register
timer.init(period=250, mode=machine.Timer.PERIODIC, callback=th)

def exampleFunction():
    print("Hello World!")
    # turns LED on for 0.5 seconds
    led.on()
    time.sleep(0.5)
    led.off()

while True:
    # if motion is detected, the example function will execute
    if msCounter > 0:
        if ms.value() == 1:
            exampleFunction()



