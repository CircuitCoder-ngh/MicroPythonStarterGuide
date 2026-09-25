# A single dot of light chasing around the ring
import time
from machine import Pin
from neopixel import NeoPixel

NUM_PIXELS = 8
pixels = NeoPixel(Pin(23), NUM_PIXELS)

position = 0
while True:
    pixels.fill((0, 0, 0))                # clear every pixel
    pixels[position] = (0, 30, 60)        # light just one
    pixels.write()
    position = (position + 1) % NUM_PIXELS   # wrap back round to 0
    time.sleep_ms(80)
