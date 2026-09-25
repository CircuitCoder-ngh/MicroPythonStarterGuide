# Print a message when motion starts and when it stops
import time
from machine import Pin

pir = Pin(33, Pin.IN)

last_value = pir.value()
count = 0

while True:
    value = pir.value()
    if value != last_value:
        if value == 1:
            count += 1
            print("Motion started! (#" + str(count) + ")")
        else:
            print("Motion stopped")
        last_value = value
    time.sleep_ms(50)
