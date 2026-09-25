# Control a motor's speed and direction with PWM
import time
from machine import Pin, PWM

IN1_PIN = 16
IN2_PIN = 17

# 20,000 pulses a second is too high-pitched to hear, so the motor won't whine
in1 = PWM(Pin(IN1_PIN), freq=20_000, duty_u16=0)
in2 = PWM(Pin(IN2_PIN), freq=20_000, duty_u16=0)


def set_motor(speed):
    # speed: -100 (full reverse) to 100 (full forward), 0 = stop
    speed = max(-100, min(100, speed))
    duty = int(abs(speed) * 65535 / 100)
    if speed > 0:
        in1.duty_u16(duty)   # pulse IN1, hold IN2 low: forwards
        in2.duty_u16(0)
    elif speed < 0:
        in1.duty_u16(0)      # pulse IN2, hold IN1 low: backwards
        in2.duty_u16(duty)
    else:
        in1.duty_u16(0)      # both low: coast
        in2.duty_u16(0)


# speed up gently, then slow down again
for speed in range(0, 101, 5):
    print("Speed", speed)
    set_motor(speed)
    time.sleep_ms(200)
for speed in range(100, -1, -5):
    set_motor(speed)
    time.sleep_ms(100)

time.sleep(1)
print("Full speed backwards")
set_motor(-100)
time.sleep(2)
set_motor(0)
