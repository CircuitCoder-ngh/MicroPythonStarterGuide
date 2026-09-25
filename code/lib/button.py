# button.py - a debounced push button you can reuse in any project.
#
# Wiring: one leg of the button to a GPIO pin, the other leg to GND.
# The internal pull-up resistor keeps the pin at 1 until the button
# is pressed, which connects it to GND and makes it read 0.
#
# Usage:
#   from button import Button
#   button = Button(14)
#   while True:
#       if button.was_pressed():
#           print("Pressed!")

import time
from machine import Pin


class Button:
    def __init__(self, pin_number, debounce_ms=30):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self._last_reading = self.pin.value()
        self._stable_value = self._last_reading
        self._changed_at = time.ticks_ms()
        self._pressed = False

    def _update(self):
        # Only trust a new reading once it has stayed the same for
        # debounce_ms. That ignores the "bounces" a button makes
        # for a few milliseconds when it is pushed or released.
        reading = self.pin.value()
        now = time.ticks_ms()
        if reading != self._last_reading:
            self._last_reading = reading
            self._changed_at = now
        elif (reading != self._stable_value
              and time.ticks_diff(now, self._changed_at) >= self.debounce_ms):
            self._stable_value = reading
            if reading == 0:
                self._pressed = True

    def was_pressed(self):
        # True once for each push, no matter how long it is held down.
        self._update()
        if self._pressed:
            self._pressed = False
            return True
        return False

    def is_down(self):
        # True for as long as the button is held down.
        self._update()
        return self._stable_value == 0
