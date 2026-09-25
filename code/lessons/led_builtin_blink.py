# Blink the LED that's built into the ESP32 board (no wiring needed!)
import time
from machine import Pin

led = Pin(2, Pin.OUT)  # most ESP32 DevKit boards have an LED on GPIO 2

while True:
    led.on()
    time.sleep(1)  # wait 1 second
    led.off()
    time.sleep(1)
