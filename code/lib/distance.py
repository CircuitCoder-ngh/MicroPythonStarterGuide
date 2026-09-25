# distance.py - measure distance with an HC-SR04 ultrasonic sensor.
#
# Wiring (see the Ultrasonic Sensors lesson):
#   VCC -> 3V3 (HC-SR04P / 3.3 V version) or VIN (classic 5 V HC-SR04)
#   TRIG -> GPIO 5
#   ECHO -> GPIO 39 (through a voltage divider if the sensor runs on 5 V)
#   GND -> GND
#
# Usage:
#   from distance import DistanceSensor
#   sensor = DistanceSensor(trigger_pin=5, echo_pin=39)
#   print(sensor.distance_cm())   # a number, or None if nothing was in range

import time
from machine import Pin, time_pulse_us

# Sound travels about 0.0343 cm per microsecond. The echo time covers the
# trip there AND back, so we halve it.
CM_PER_MICROSECOND = 0.0343 / 2

# The sensor needs a short rest between measurements, or it can hear the
# echo of the previous ping.
MIN_GAP_MS = 60


class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin, max_cm=250):
        self.trigger = Pin(trigger_pin, Pin.OUT, value=0)
        self.echo = Pin(echo_pin, Pin.IN)
        # Longest echo worth waiting for, plus a little extra
        self.timeout_us = int(max_cm / CM_PER_MICROSECOND) + 2000
        self._last_ping = time.ticks_ms() - MIN_GAP_MS

    def distance_cm(self):
        # Wait if we pinged too recently
        wait = MIN_GAP_MS - time.ticks_diff(time.ticks_ms(), self._last_ping)
        if wait > 0:
            time.sleep_ms(wait)

        # A 10 microsecond pulse on TRIG tells the sensor to send a ping
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        self._last_ping = time.ticks_ms()

        # ECHO goes high for as long as the sound took to come back
        duration = time_pulse_us(self.echo, 1, self.timeout_us)
        if duration < 0:
            return None   # no echo: nothing in range
        return round(duration * CM_PER_MICROSECOND, 1)
