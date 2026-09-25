# Each press of Button A moves the servo to the next position
from machine import PWM, Pin
from button import Button

SERVO_MIN_NS = 500_000
SERVO_MAX_NS = 2_500_000
POSITIONS = [0, 45, 90, 135, 180]

servo = PWM(Pin(13), freq=50, duty_u16=0)
button = Button(14)


def set_angle(angle):
    angle = max(0, min(180, angle))
    pulse = SERVO_MIN_NS + (SERVO_MAX_NS - SERVO_MIN_NS) * angle // 180
    servo.duty_ns(pulse)


index = 0
set_angle(POSITIONS[index])

while True:
    if button.was_pressed():
        index = (index + 1) % len(POSITIONS)   # wrap back to 0 at the end
        print("Angle:", POSITIONS[index])
        set_angle(POSITIONS[index])
