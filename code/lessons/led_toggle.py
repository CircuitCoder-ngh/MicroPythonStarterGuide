# Flip an LED between on and off, faster and faster
import time
from machine import Pin

LED_PIN = 27

led = Pin(LED_PIN, Pin.OUT)

delay = 1.0
while delay > 0.05:
    led.value(not led.value())   # on becomes off, off becomes on
    time.sleep(delay)
    delay = delay * 0.9   # shrink the delay by 10% every time

led.off()
print("Done!")
