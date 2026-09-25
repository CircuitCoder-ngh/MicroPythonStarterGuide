# Measure distance using the DistanceSensor class from distance.py
# (copy distance.py onto your ESP32 first)
import time
from distance import DistanceSensor

sensor = DistanceSensor(trigger_pin=5, echo_pin=39)

while True:
    cm = sensor.distance_cm()
    if cm is None:
        print("Nothing in range")
    else:
        print(cm, "cm")
    time.sleep_ms(200)
