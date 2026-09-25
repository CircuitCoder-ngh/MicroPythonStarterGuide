# Calibrate the light sensor, then show a 0-100 % light level
# that uses the full range of YOUR room's lighting
import time
from machine import ADC, Pin

LDR_PIN = 36

ldr = ADC(Pin(LDR_PIN), atten=ADC.ATTN_11DB)

# For 5 seconds, cover the sensor and shine a light on it
# so the code can learn the darkest and brightest readings
print("Calibrating for 5 seconds: cover the sensor, then uncover it!")
darkest = 65535
brightest = 0
start = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start) < 5000:
    reading = ldr.read_u16()
    darkest = min(darkest, reading)
    brightest = max(brightest, reading)
print("Darkest:", darkest, " Brightest:", brightest)

if brightest - darkest < 1000:
    brightest = darkest + 1000   # not much change seen: avoid dividing by ~0

while True:
    reading = ldr.read_u16()
    level = (reading - darkest) * 100 // (brightest - darkest)
    level = max(0, min(100, level))   # keep it between 0 and 100
    print("Light level:", level, "%")
    time.sleep(0.3)
