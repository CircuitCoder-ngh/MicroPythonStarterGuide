# Mix any colour on an RGB LED using PWM
import time
from machine import PWM, Pin

red = PWM(Pin(16), freq=1000, duty_u16=0)
green = PWM(Pin(17), freq=1000, duty_u16=0)
blue = PWM(Pin(18), freq=1000, duty_u16=0)


def set_colour(r, g, b):
    # r, g and b go from 0 (off) to 255 (full brightness),
    # the same way colours are written on web pages
    red.duty_u16(r * 257)      # 255 * 257 = 65535, the maximum duty
    green.duty_u16(g * 257)
    blue.duty_u16(b * 257)


set_colour(255, 80, 0)     # orange
time.sleep(2)
set_colour(120, 0, 255)    # purple
time.sleep(2)
set_colour(0, 0, 0)        # off
