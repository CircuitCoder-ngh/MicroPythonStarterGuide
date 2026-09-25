# Read a light sensor (photoresistor) and print how bright it is
import time
from machine import ADC, Pin

LDR_PIN = 36   # often labelled VP on the board

ldr = ADC(Pin(LDR_PIN), atten=ADC.ATTN_11DB)

while True:
    raw = ldr.read_u16()          # 0 (dark) to 65535 (very bright)
    percent = raw * 100 // 65535
    print("Light:", raw, "=", percent, "%")
    time.sleep(0.5)
