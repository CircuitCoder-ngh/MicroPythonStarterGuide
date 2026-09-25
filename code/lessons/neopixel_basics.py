# Light up a NeoPixel ring or stick, one colour per pixel
from machine import Pin
from neopixel import NeoPixel

NEOPIXEL_PIN = 23
NUM_PIXELS = 8          # change this to match your ring or stick

pixels = NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# Colours are (red, green, blue), each from 0 to 255.
# Keeping them low (under ~64) saves power and your eyes!
pixels[0] = (40, 0, 0)     # red
pixels[1] = (0, 40, 0)     # green
pixels[2] = (0, 0, 40)     # blue
pixels[3] = (40, 40, 0)    # yellow
pixels[4] = (0, 40, 40)    # cyan
pixels[5] = (40, 0, 40)    # magenta
pixels[6] = (40, 40, 40)   # white
pixels[7] = (0, 0, 0)      # off

pixels.write()   # nothing changes until you call write()
