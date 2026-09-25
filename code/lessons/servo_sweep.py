# Move a servo to 0, 90 and 180 degrees, then sweep smoothly
import time
from machine import PWM, Pin

SERVO_PIN = 13

# Pulse lengths (in nanoseconds) for 0 and 180 degrees.
# Adjust these if your servo doesn't reach the ends (see servo_calibrate.py)
SERVO_MIN_NS = 500_000     # 0.5 ms
SERVO_MAX_NS = 2_500_000   # 2.5 ms

# Servos expect a pulse 50 times a second (50 Hz)
servo = PWM(Pin(SERVO_PIN), freq=50, duty_u16=0)


def set_angle(angle):
    angle = max(0, min(180, angle))   # keep it between 0 and 180
    pulse = SERVO_MIN_NS + (SERVO_MAX_NS - SERVO_MIN_NS) * angle // 180
    servo.duty_ns(pulse)


for angle in (0, 90, 180):
    print("Moving to", angle)
    set_angle(angle)
    time.sleep(1)

# sweep back down 2 degrees at a time
for angle in range(180, -1, -2):
    set_angle(angle)
    time.sleep_ms(20)

servo.duty_u16(0)   # stop sending pulses: the servo relaxes
