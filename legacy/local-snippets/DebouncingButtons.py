import machine
import time

buttonCounter = 0

BUTTON_PIN = 14 # can be any pin that isn't affected by pull-up resistor

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# In functions, variables must be defined as global if it is altered
# within the function, and then used outside of the function.
# Otherwise, the changes made to that variable within the function 
# wouldn't remain after the function executes

def th(timer): # errors will occur without timer parameter
    global buttonCounter
    if buttonCounter == 0:
        buttonCounter += 1

timer = machine.Timer(-1) # creates the timer
timer.init(period=100, mode=machine.Timer.PERIODIC, callback=th)
# period is defined in milliseconds (100ms = 0.1s)
# mode can be .PERIODIC or .ONE_SHOT
# callback is the function that executes when timer is called
# (callback function must be kept short or else bugs can occur)

def example_function():
    print('Hello World!')

while True:
    if buttonCounter > 0:
        if button.value() == 0:
            example_function()
            buttonCounter -= 1

