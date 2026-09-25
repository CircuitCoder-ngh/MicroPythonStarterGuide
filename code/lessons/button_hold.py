# The LED stays on only while Button A is held down,
# and a message is printed each time it's pressed
from machine import Pin
from button import Button

led = Pin(27, Pin.OUT)
button = Button(14)

while True:
    if button.was_pressed():
        print("Pressed!")
    led.value(button.is_down())
