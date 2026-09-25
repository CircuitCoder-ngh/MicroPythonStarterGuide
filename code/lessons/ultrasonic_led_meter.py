# Closer objects light the RGB LED red, far ones green
import time
from machine import Pin
from distance import DistanceSensor

sensor = DistanceSensor(trigger_pin=5, echo_pin=39)
red = Pin(16, Pin.OUT)
green = Pin(17, Pin.OUT)
blue = Pin(18, Pin.OUT)
blue.off()

while True:
    cm = sensor.distance_cm()
    if cm is not None and cm < 20:
        red.on()        # too close!
        green.off()
    elif cm is not None and cm < 50:
        red.on()        # red + green = yellow: getting close
        green.on()
    else:
        red.off()       # all clear
        green.on()
    time.sleep_ms(100)
