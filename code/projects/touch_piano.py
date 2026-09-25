# Touch Piano: seven touch keys play a scale on the buzzer.
# Keys can be foil squares, coins, or even pieces of fruit!
import time
from machine import Pin, PWM, TouchPad

BUZZER_PIN = 26
VOLUME = 32768      # duty_u16: 0 is silent, 32768 (50%) is loudest
SENSITIVITY = 0.7   # a key counts as touched below 70% of its baseline

# (note name, touch pin, frequency in Hz), lowest note first
KEYS = [
    ("C", 4, 262),
    ("D", 15, 294),
    ("E", 13, 330),
    ("F", 14, 349),
    ("G", 27, 392),
    ("A", 33, 440),
    ("B", 32, 494),
]

# Optional: light a NeoPixel stick in a different colour for each note.
# Set USE_PIXELS = True if you have one plugged into GPIO 23.
USE_PIXELS = False
PIXEL_PIN = 23
NUM_PIXELS = 8
COLOURS = [(60, 0, 0), (60, 25, 0), (60, 60, 0), (0, 60, 0),
           (0, 50, 60), (0, 0, 60), (40, 0, 60)]

# Step 1: set up each component
buzzer = PWM(Pin(BUZZER_PIN), freq=262, duty_u16=0)
pads = [TouchPad(Pin(pin)) for name, pin, freq in KEYS]

pixels = None
if USE_PIXELS:
    from neopixel import NeoPixel
    pixels = NeoPixel(Pin(PIXEL_PIN, Pin.OUT), NUM_PIXELS)


# Step 2: small functions for each job
def calibrate():
    # Learn what each key reads when nobody is touching it
    print("Calibrating... keep your hands off the keys!")
    baselines = []
    for pad in pads:
        total = 0
        for i in range(20):
            total += pad.read()
            time.sleep_ms(5)
        baselines.append(total // 20)
    print("Baselines:", baselines)
    return baselines


def pressed_key():
    # Return the index of the lowest touched key, or None
    for i in range(len(pads)):
        if pads[i].read() < baselines[i] * SENSITIVITY:
            return i
    return None


def show_colour(key):
    if pixels is None:
        return
    colour = (0, 0, 0) if key is None else COLOURS[key]
    for i in range(NUM_PIXELS):
        pixels[i] = colour
    pixels.write()


# Step 3: play whichever key is being touched
baselines = calibrate()
print("Ready! Touch a key.")
current = None

while True:
    key = pressed_key()
    if key != current:           # only act when something changes
        if key is None:
            buzzer.duty_u16(0)
        else:
            name, pin, freq = KEYS[key]
            buzzer.freq(freq)
            buzzer.duty_u16(VOLUME)
            print(name)
        show_colour(key)
        current = key
    time.sleep_ms(10)
