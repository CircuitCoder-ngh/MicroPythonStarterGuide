# Measure distance with an HC-SR04, step by step
import time
from machine import Pin, time_pulse_us

TRIG_PIN = 5
ECHO_PIN = 39   # often labelled VN on the board

trigger = Pin(TRIG_PIN, Pin.OUT, value=0)
echo = Pin(ECHO_PIN, Pin.IN)

while True:
    # 1. Send a 10 microsecond pulse to make the sensor "ping"
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    # 2. Time how long ECHO stays high: that's how long the sound
    #    took to reach the object and bounce back
    duration = time_pulse_us(echo, 1, 30000)   # give up after 30 ms

    if duration < 0:
        print("Nothing in range")
    else:
        # 3. Sound travels 0.0343 cm per microsecond. Halve it,
        #    because the sound went there AND back.
        distance = duration * 0.0343 / 2
        print(f"{distance:.1f} cm")

    time.sleep_ms(200)
