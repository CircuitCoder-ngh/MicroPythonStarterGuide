# Blink an LED wired to GPIO 27
import time
from machine import Pin

LED_PIN = 27  # any pin that's OK for output (see the ESP32 Pins page)

led = Pin(LED_PIN, Pin.OUT)

while True:
    led.on()        # send 3.3 V out of the pin: current flows, the LED lights
    time.sleep(1)
    led.off()       # back to 0 V: no current, the LED goes dark
    time.sleep(1)
