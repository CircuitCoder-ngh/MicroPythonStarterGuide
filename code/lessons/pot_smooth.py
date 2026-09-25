# Smooth out a jittery potentiometer by averaging several readings
import time
from machine import ADC, Pin

POT_PIN = 34

pot = ADC(Pin(POT_PIN), atten=ADC.ATTN_11DB)


def read_average(adc, samples=16):
    total = 0
    for i in range(samples):
        total += adc.read_u16()
    return total // samples


while True:
    percent = read_average(pot) * 100 // 65535
    print(percent, "%")
    time.sleep(0.2)
