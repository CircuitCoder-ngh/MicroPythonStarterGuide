# A rainbow that spins around the ring
import time
from machine import Pin
from neopixel import NeoPixel

NUM_PIXELS = 8
BRIGHTNESS = 0.25   # 0.0 to 1.0

pixels = NeoPixel(Pin(23), NUM_PIXELS)


def wheel(position):
    # Turn a number from 0-255 into a colour on the colour wheel:
    # red -> green -> blue -> back to red
    position = position % 256
    if position < 85:
        r, g, b = 255 - position * 3, position * 3, 0
    elif position < 170:
        position -= 85
        r, g, b = 0, 255 - position * 3, position * 3
    else:
        position -= 170
        r, g, b = position * 3, 0, 255 - position * 3
    return (int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))


offset = 0
while True:
    for i in range(NUM_PIXELS):
        # spread the whole rainbow evenly around the ring
        pixels[i] = wheel(i * 256 // NUM_PIXELS + offset)
    pixels.write()
    offset += 4
    time.sleep_ms(30)
