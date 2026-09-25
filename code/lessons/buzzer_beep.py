# Beep a piezo buzzer three times
import time
from machine import PWM, Pin

BUZZER_PIN = 26

buzzer = PWM(Pin(BUZZER_PIN), freq=1000, duty_u16=0)  # starts silent

for i in range(3):
    buzzer.duty_u16(32768)   # 50% duty: loudest
    time.sleep(0.2)
    buzzer.duty_u16(0)       # 0% duty: silent
    time.sleep(0.2)

buzzer.deinit()   # release the pin
