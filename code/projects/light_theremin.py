# Light Theremin: wave your hand over the light sensor to change the pitch.
# Button A mutes and unmutes the sound.
import time
from machine import Pin, PWM, ADC
from button import Button

LIGHT_PIN = 36    # light sensor (LDR + 10 kΩ divider)
BUZZER_PIN = 26
BUTTON_PIN = 14   # Button A

LOWEST_NOTE = 150    # Hz, when the sensor is at its darkest
HIGHEST_NOTE = 1500  # Hz, when the sensor is at its brightest
VOLUME = 32768       # duty_u16: 0 is silent, 32768 (50%) is loudest
CALIBRATE_MS = 5000  # how long to spend learning the light levels

# Step 1: set up each component
light = ADC(Pin(LIGHT_PIN), atten=ADC.ATTN_11DB)
buzzer = PWM(Pin(BUZZER_PIN), freq=LOWEST_NOTE, duty_u16=0)
button = Button(BUTTON_PIN)
onboard_led = Pin(2, Pin.OUT)

muted = False


# Step 2: break the job into small functions
def calibrate():
    # For 5 seconds, record the darkest and brightest readings we see.
    # Wave your hand up and down over the sensor while the LED is on!
    print("Calibrating: wave your hand over the sensor...")
    onboard_led.on()
    darkest = 65535
    brightest = 0
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < CALIBRATE_MS:
        reading = light.read_u16()
        darkest = min(darkest, reading)
        brightest = max(brightest, reading)
        time.sleep_ms(5)
    onboard_led.off()
    if brightest - darkest < 1000:
        # hardly any change: fall back to the full range
        darkest, brightest = 0, 65535
    print("Darkest:", darkest, "Brightest:", brightest)
    return darkest, brightest


def light_to_pitch(reading, darkest, brightest):
    # keep the reading inside the calibrated range...
    reading = max(darkest, min(brightest, reading))
    # ...then map it onto our range of notes
    span = brightest - darkest
    return LOWEST_NOTE + (reading - darkest) * (HIGHEST_NOTE - LOWEST_NOTE) // span


def toggle_mute():
    global muted
    muted = not muted
    print("Muted" if muted else "Playing")


# Step 3: calibrate once, then play forever
darkest, brightest = calibrate()
buzzer.duty_u16(VOLUME)

while True:
    if button.was_pressed():
        toggle_mute()

    if muted:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(light_to_pitch(light.read_u16(), darkest, brightest))
        buzzer.duty_u16(VOLUME)
    time.sleep_ms(10)
