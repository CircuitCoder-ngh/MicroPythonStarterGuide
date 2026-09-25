# A siren that sweeps up and down in pitch
import time
from machine import PWM, Pin

buzzer = PWM(Pin(26), freq=600, duty_u16=32768)

for repeat in range(5):
    for frequency in range(600, 1500, 20):     # rising
        buzzer.freq(frequency)
        time.sleep_ms(5)
    for frequency in range(1500, 600, -20):    # falling
        buzzer.freq(frequency)
        time.sleep_ms(5)

buzzer.deinit()
