# Show whether the room is comfortable using the RGB LED:
# blue = too cold, green = just right, red = too hot
import time
import dht
from machine import Pin

TOO_COLD = 18   # °C
TOO_HOT = 26    # °C

sensor = dht.DHT11(Pin(19))
red = Pin(16, Pin.OUT)
green = Pin(17, Pin.OUT)
blue = Pin(18, Pin.OUT)


def show(r, g, b):
    red.value(r)
    green.value(g)
    blue.value(b)


while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        print("Temperature:", temp, "°C")
        if temp < TOO_COLD:
            show(0, 0, 1)
        elif temp > TOO_HOT:
            show(1, 0, 0)
        else:
            show(0, 1, 0)
    except OSError:
        print("Sensor read failed, trying again")
    time.sleep(2)
