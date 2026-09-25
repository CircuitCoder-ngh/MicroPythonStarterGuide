# Print what a button's pin reads, 10 times a second
import time
from machine import Pin

BUTTON_PIN = 14  # Button A

# PULL_UP keeps the pin at 1 until the button connects it to GND
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

while True:
    print(button.value())   # 1 = not pressed, 0 = pressed
    time.sleep(0.1)
