# Parking Sensor: beeps faster and glows redder as something gets closer,
# just like the sensors on the back of a car.
import time
from machine import Pin, PWM
from distance import DistanceSensor

BUZZER_PIN = 26
RED_PIN, GREEN_PIN, BLUE_PIN = 16, 17, 18

FAR_CM = 50      # further than this: green, no beeping
NEAR_CM = 25     # closer than FAR_CM: yellow, slow beeps
STOP_CM = 10     # closer than this: red, one continuous tone
BEEP_HZ = 1000
VOLUME = 32768
BEEP_LENGTH_MS = 60

# Step 1: set up each component
sensor = DistanceSensor(trigger_pin=5, echo_pin=39)
buzzer = PWM(Pin(BUZZER_PIN), freq=BEEP_HZ, duty_u16=0)
red = PWM(Pin(RED_PIN), freq=1000, duty_u16=0)
green = PWM(Pin(GREEN_PIN), freq=1000, duty_u16=0)
blue = PWM(Pin(BLUE_PIN), freq=1000, duty_u16=0)

readings = []          # the last three distances, for smoothing
last_beep = time.ticks_ms()


# Step 2: small functions for each job
def set_colour(r, g, b):
    # r, g and b go from 0 (off) to 255 (full brightness)
    red.duty_u16(r * 257)
    green.duty_u16(g * 257)
    blue.duty_u16(b * 257)


def smoothed_distance():
    # The median (middle value) of the last three readings ignores
    # the odd wild measurement. Returns None until we have readings.
    cm = sensor.distance_cm()
    if cm is not None:
        readings.append(cm)
        if len(readings) > 3:
            readings.pop(0)
    if not readings:
        return None
    return sorted(readings)[len(readings) // 2]


def beep_gap_ms(cm):
    # The closer you are, the shorter the gap between beeps:
    # 600 ms at NEAR_CM (or further), down to 80 ms at STOP_CM
    cm = max(STOP_CM, min(NEAR_CM, cm))
    return 80 + (cm - STOP_CM) * (600 - 80) // (NEAR_CM - STOP_CM)


def update(cm):
    global last_beep
    now = time.ticks_ms()

    if cm is None or cm > FAR_CM:
        set_colour(0, 255, 0)           # green: all clear
        buzzer.duty_u16(0)
    elif cm < STOP_CM:
        set_colour(255, 0, 0)           # red: STOP!
        buzzer.duty_u16(VOLUME)         # continuous tone
    else:
        if cm < NEAR_CM:
            set_colour(255, 0, 0)       # red: getting close
        else:
            set_colour(255, 120, 0)     # yellow: careful
        # beep for BEEP_LENGTH_MS, then stay quiet until the gap is over
        since = time.ticks_diff(now, last_beep)
        if since >= beep_gap_ms(cm):
            last_beep = now
            since = 0
        buzzer.duty_u16(VOLUME if since < BEEP_LENGTH_MS else 0)


# Step 3: measure and react, over and over
while True:
    cm = smoothed_distance()
    update(cm)
    if cm is not None:
        print(cm, "cm")
