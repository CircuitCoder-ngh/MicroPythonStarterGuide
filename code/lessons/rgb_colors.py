# Cycle an RGB LED through red, green, blue and some mixed colours
import time
from machine import Pin

red = Pin(16, Pin.OUT)
green = Pin(17, Pin.OUT)
blue = Pin(18, Pin.OUT)


def show(r, g, b):
    # each argument is 1 (on) or 0 (off)
    red.value(r)
    green.value(g)
    blue.value(b)


COLOURS = [
    ("red", 1, 0, 0),
    ("green", 0, 1, 0),
    ("blue", 0, 0, 1),
    ("yellow", 1, 1, 0),
    ("cyan", 0, 1, 1),
    ("magenta", 1, 0, 1),
    ("white", 1, 1, 1),
]

while True:
    for name, r, g, b in COLOURS:
        print(name)
        show(r, g, b)
        time.sleep(1)
