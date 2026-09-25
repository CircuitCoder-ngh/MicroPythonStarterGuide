# Fade smoothly around the colour wheel: red -> green -> blue -> red
import time
from machine import PWM, Pin

red = PWM(Pin(16), freq=1000, duty_u16=0)
green = PWM(Pin(17), freq=1000, duty_u16=0)
blue = PWM(Pin(18), freq=1000, duty_u16=0)


def set_colour(r, g, b):
    red.duty_u16(r * 257)
    green.duty_u16(g * 257)
    blue.duty_u16(b * 257)


while True:
    for step in range(256):         # red fades out, green fades in
        set_colour(255 - step, step, 0)
        time.sleep_ms(8)
    for step in range(256):         # green fades out, blue fades in
        set_colour(0, 255 - step, step)
        time.sleep_ms(8)
    for step in range(256):         # blue fades out, red fades in
        set_colour(step, 0, 255 - step)
        time.sleep_ms(8)
