# Sweep through frequencies to hear how pitch changes
import time
from machine import PWM, Pin

BUZZER_PIN = 26

buzzer = PWM(Pin(BUZZER_PIN), freq=100, duty_u16=32768)

# start at 100 Hz, go up by 50 Hz each step, stop before 2000 Hz
for frequency in range(100, 2000, 50):
    print(frequency, "Hz")
    buzzer.freq(frequency)
    time.sleep(0.2)

buzzer.duty_u16(0)
buzzer.deinit()
