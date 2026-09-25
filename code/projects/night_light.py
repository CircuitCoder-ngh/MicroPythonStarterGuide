# Night Light: a NeoPixel ring that switches itself on when the room
# gets dark. Touch the pad on GPIO 4 to change the lighting mode.
import time
from machine import Pin, ADC, TouchPad
from neopixel import NeoPixel

LIGHT_PIN = 36     # light sensor (LDR + 10 kΩ divider)
PIXEL_PIN = 23     # NeoPixel DIN
NUM_PIXELS = 8
TOUCH_PIN = 4      # touch pad

# The light only switches on below DARK and off above BRIGHT. The gap
# between them (hysteresis) stops it flickering at dusk.
DARK = 15000
BRIGHT = 22000
BRIGHTNESS = 0.4   # 0.0 to 1.0: NeoPixels are VERY bright

MODES = ["auto warm white", "rainbow", "colour fade", "off"]

# Step 1: set up each component
light = ADC(Pin(LIGHT_PIN), atten=ADC.ATTN_11DB)
pixels = NeoPixel(Pin(PIXEL_PIN, Pin.OUT), NUM_PIXELS)
touch = TouchPad(Pin(TOUCH_PIN))

mode = 0
is_dark = False
level = 0.0          # current fade level, 0.0 (off) to 1.0 (full)
step = 0             # animation counter
touch_baseline = 0
was_touched = False


# Step 2: small functions for each job
def calibrate_touch():
    # Average a few readings with nobody touching the pad
    total = 0
    for i in range(20):
        total += touch.read()
        time.sleep_ms(10)
    return total // 20


def touched():
    # On the ESP32, the reading DROPS when you touch the pad
    return touch.read() < touch_baseline * 0.7


def check_touch():
    # Change mode once per touch (not over and over while held)
    global was_touched, mode
    now = touched()
    if now and not was_touched:
        mode = (mode + 1) % len(MODES)
        print("Mode:", MODES[mode])
    was_touched = now


def check_darkness():
    global is_dark
    reading = light.read_u16()
    if reading < DARK:
        is_dark = True
    elif reading > BRIGHT:
        is_dark = False


def wheel(position):
    # Turn a number from 0-255 into a colour of the rainbow
    position = position % 256
    if position < 85:
        return (255 - position * 3, position * 3, 0)
    if position < 170:
        position -= 85
        return (0, 255 - position * 3, position * 3)
    position -= 170
    return (position * 3, 0, 255 - position * 3)


def scaled(colour, amount):
    r, g, b = colour
    return (int(r * amount), int(g * amount), int(b * amount))


def draw():
    # Fill the ring with the current mode's colours, faded by `level`
    amount = level * BRIGHTNESS
    for i in range(NUM_PIXELS):
        if mode == 0:
            colour = (255, 140, 40)          # warm white
        elif mode == 1:
            colour = wheel(step + i * 256 // NUM_PIXELS)
        else:
            colour = wheel(step // 2)        # the whole ring, one colour
        pixels[i] = scaled(colour, amount)
    pixels.write()


# Step 3: the main loop
touch_baseline = calibrate_touch()
print("Touch baseline:", touch_baseline)

while True:
    check_touch()
    check_darkness()

    # Work out how bright we SHOULD be...
    if MODES[mode] == "off":
        target = 0.0
    elif mode == 0:
        target = 1.0 if is_dark else 0.0   # only warm white is automatic
    else:
        target = 1.0

    # ...and fade towards it a little each loop, for smooth changes
    if level < target:
        level = min(target, level + 0.02)
    elif level > target:
        level = max(target, level - 0.02)

    draw()
    step += 1
    time.sleep_ms(20)
