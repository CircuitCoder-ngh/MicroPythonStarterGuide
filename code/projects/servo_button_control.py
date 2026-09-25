# Servo Controller (button version):
# Button A turns the servo one way, Button B turns it the other way.
# Tap for 1 degree, or hold the button down to keep moving.
import time
from machine import Pin, PWM
from button import Button

SERVO_PIN = 13
BUTTON_A_PIN = 14
BUTTON_B_PIN = 25

SERVO_MIN_NS = 500_000     # pulse width for 0 degrees
SERVO_MAX_NS = 2_500_000   # pulse width for 180 degrees
HOLD_DELAY_MS = 400        # how long to hold before it starts repeating
REPEAT_MS = 50             # while held, move 1 degree this often

servo = PWM(Pin(SERVO_PIN), freq=50, duty_u16=0)
button_a = Button(BUTTON_A_PIN)
button_b = Button(BUTTON_B_PIN)

angle = 90                 # start in the middle
held_since = 0             # when the current hold started
last_step = 0              # when we last moved while holding


def set_angle(new_angle):
    pulse = SERVO_MIN_NS + (SERVO_MAX_NS - SERVO_MIN_NS) * new_angle // 180
    servo.duty_ns(pulse)


def move(step):
    global angle
    # clamp keeps the angle between 0 and 180
    new_angle = max(0, min(180, angle + step))
    if new_angle != angle:
        angle = new_angle
        set_angle(angle)
        print("Angle:", angle)


def check_button(button, step):
    global held_since, last_step
    now = time.ticks_ms()
    if button.was_pressed():
        move(step)                 # a tap moves 1 degree
        held_since = now
        last_step = now
    elif button.is_down():
        held_for = time.ticks_diff(now, held_since)
        since_step = time.ticks_diff(now, last_step)
        if held_for > HOLD_DELAY_MS and since_step >= REPEAT_MS:
            move(step)             # still held: keep moving
            last_step = now


set_angle(angle)

while True:
    check_button(button_a, -1)
    check_button(button_b, +1)
    time.sleep_ms(5)
