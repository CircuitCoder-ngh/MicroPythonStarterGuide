# Light the LED whenever the motion sensor sees movement
import time
from machine import Pin

PIR_PIN = 33
LED_PIN = 27

pir = Pin(PIR_PIN, Pin.IN)   # the sensor drives the pin itself: no pull-up needed
led = Pin(LED_PIN, Pin.OUT)

print("Warming up... give the sensor about a minute to settle")

while True:
    led.value(pir.value())   # 1 = motion, 0 = no motion
    time.sleep_ms(50)
