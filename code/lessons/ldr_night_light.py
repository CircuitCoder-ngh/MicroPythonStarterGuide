# Turn the LED on automatically when it gets dark
import time
from machine import ADC, Pin

LDR_PIN = 36
LED_PIN = 27
DARK_BELOW = 15000   # adjust using the readings from ldr_read.py

ldr = ADC(Pin(LDR_PIN), atten=ADC.ATTN_11DB)
led = Pin(LED_PIN, Pin.OUT)

while True:
    reading = ldr.read_u16()
    if reading < DARK_BELOW:
        led.on()
    else:
        led.off()
    time.sleep(0.2)
