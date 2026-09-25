# Each press of Button A turns the LED on or off
from machine import Pin
from button import Button

LED_PIN = 27
BUTTON_PIN = 14

led = Pin(LED_PIN, Pin.OUT)
button = Button(BUTTON_PIN)

while True:
    if button.was_pressed():
        led.value(not led.value())   # flip the LED
