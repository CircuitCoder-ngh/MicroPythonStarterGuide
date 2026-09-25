# Count button presses, ignoring the "bounces"
import time
from machine import Pin

BUTTON_PIN = 14

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

last_value = button.value()
presses = 0

while True:
    value = button.value()
    if value != last_value:      # the button just changed
        if value == 0:           # ...and it changed to pressed
            presses += 1
            print("Pressed! Total:", presses)
        last_value = value
        time.sleep_ms(20)        # ignore the bouncing for 20 ms
