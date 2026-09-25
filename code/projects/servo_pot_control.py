# Servo Controller (potentiometer version):
# the servo arm follows the potentiometer dial.
import time
from machine import Pin, PWM, ADC

SERVO_PIN = 13
POT_PIN = 34      # Potentiometer 1

# Pulse widths for 0 and 180 degrees. Adjust these if your servo
# doesn't reach the full range or buzzes at the ends.
SERVO_MIN_NS = 500_000     # 0.5 ms
SERVO_MAX_NS = 2_500_000   # 2.5 ms

servo = PWM(Pin(SERVO_PIN), freq=50, duty_u16=0)
pot = ADC(Pin(POT_PIN), atten=ADC.ATTN_11DB)


def set_angle(angle):
    pulse = SERVO_MIN_NS + (SERVO_MAX_NS - SERVO_MIN_NS) * angle // 180
    servo.duty_ns(pulse)


def read_pot_angle():
    # Average a few readings: the ADC is a little noisy, and without
    # this the servo would twitch even when you aren't touching the dial.
    total = 0
    for _ in range(8):
        total += pot.read_u16()
    average = total // 8
    return average * 180 // 65535


current_angle = -1  # -1 means "not set yet"

while True:
    angle = read_pot_angle()
    # only move the servo when the dial has really changed
    if abs(angle - current_angle) >= 1:
        set_angle(angle)
        current_angle = angle
    time.sleep_ms(20)
