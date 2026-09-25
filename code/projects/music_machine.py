# Music Machine: Button A turns the sound on and off,
# Potentiometer 1 changes the pitch.
import time
from machine import Pin, PWM, ADC
from button import Button

BUTTON_PIN = 14   # Button A
BUZZER_PIN = 26
POT_PIN = 34      # Potentiometer 1

LOWEST_NOTE = 200    # Hz, with the dial turned all the way down
HIGHEST_NOTE = 2000  # Hz, with the dial turned all the way up
VOLUME = 32768       # duty_u16: 0 is silent, 32768 (50%) is loudest

# Step 1: set up each component
button = Button(BUTTON_PIN)
buzzer = PWM(Pin(BUZZER_PIN), freq=LOWEST_NOTE, duty_u16=0)
pot = ADC(Pin(POT_PIN), atten=ADC.ATTN_11DB)  # read the full 0-3.3 V range

playing = False


# Step 2: break the job into small functions
def toggle_sound():
    global playing
    playing = not playing
    if playing:
        buzzer.duty_u16(VOLUME)
    else:
        buzzer.duty_u16(0)


def update_pitch():
    reading = pot.read_u16()  # 0 to 65535
    # scale the reading onto our range of notes
    frequency = LOWEST_NOTE + reading * (HIGHEST_NOTE - LOWEST_NOTE) // 65535
    buzzer.freq(frequency)


# Step 3: call the functions from the main loop
while True:
    if button.was_pressed():
        toggle_sound()
    if playing:
        update_pitch()
    time.sleep_ms(10)
