# Print the raw value of a touch pin. Touch the wire and watch it change!
import time
from machine import Pin, TouchPad

TOUCH_PIN = 4

touch = TouchPad(Pin(TOUCH_PIN))

while True:
    print(touch.read())   # gets SMALLER when you touch it
    time.sleep(0.2)
