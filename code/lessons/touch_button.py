# A reusable touch "button": works out its own threshold at startup,
# then reports each new touch once, just like Button.was_pressed()
import time
from machine import Pin, TouchPad

LED_PIN = 27


class TouchButton:
    def __init__(self, pin_number, sensitivity=0.7):
        self.pad = TouchPad(Pin(pin_number))
        # Measure the untouched value a few times and average it.
        # Don't touch the pad while the program starts!
        total = 0
        for i in range(10):
            total += self.pad.read()
            time.sleep_ms(20)
        baseline = total // 10
        # A touch drops the reading well below the baseline
        self.threshold = int(baseline * sensitivity)
        self._was_down = False

    def is_touched(self):
        return self.pad.read() < self.threshold

    def was_touched(self):
        # True once each time a finger lands on the pad
        down = self.is_touched()
        new_touch = down and not self._was_down
        self._was_down = down
        return new_touch


led = Pin(LED_PIN, Pin.OUT)
pad_a = TouchButton(4)
pad_b = TouchButton(15)
print("Ready: touch the wire on GPIO 4 or GPIO 15")

while True:
    if pad_a.was_touched():
        led.value(not led.value())   # pad A toggles the LED
        print("Pad A: LED", "on" if led.value() else "off")
    if pad_b.was_touched():
        print("Pad B touched!")
    time.sleep_ms(20)
