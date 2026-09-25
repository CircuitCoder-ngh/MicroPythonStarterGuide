# Fortune Teller: press Button A and the servo "spins" a pointer
# across a half-circle wheel, slows down, and lands on a fortune.
import time
import random
from machine import Pin, PWM
from button import Button

SERVO_PIN = 13
BUTTON_PIN = 14    # Button A
BUZZER_PIN = 26    # optional: makes a tick sound while spinning

SERVO_MIN_NS = 500_000     # pulse width for 0 degrees
SERVO_MAX_NS = 2_500_000   # pulse width for 180 degrees

# Write these on your wheel, starting from the slice the arm
# points at when the servo is at 0 degrees.
FORTUNES = [
    "Yes!",
    "Ask again later",
    "Definitely not",
    "Without a doubt",
    "Maybe...",
    "Don't count on it",
]
SLICE_SIZE = 180 // len(FORTUNES)   # 30 degrees per slice

servo = PWM(Pin(SERVO_PIN), freq=50, duty_u16=0)
buzzer = PWM(Pin(BUZZER_PIN), freq=2000, duty_u16=0)
button = Button(BUTTON_PIN)


def set_angle(angle):
    pulse = SERVO_MIN_NS + (SERVO_MAX_NS - SERVO_MIN_NS) * angle // 180
    servo.duty_ns(pulse)


def tick():
    buzzer.duty_u16(32768)
    time.sleep_ms(3)
    buzzer.duty_u16(0)


def spin():
    spin_time = random.randint(2000, 6000)   # 2 to 6 seconds
    start = time.ticks_ms()
    angle = 0
    direction = 1
    while True:
        elapsed = time.ticks_diff(time.ticks_ms(), start)
        if elapsed >= spin_time:
            break
        # the step shrinks from 10 degrees to 1 degree, so it slows down
        step = 10 - 9 * elapsed // spin_time
        old_slice = angle // SLICE_SIZE
        angle += step * direction
        if angle >= 180:          # bounce off the ends of the wheel
            angle = 180
            direction = -1
        elif angle <= 0:
            angle = 0
            direction = 1
        set_angle(angle)
        if angle // SLICE_SIZE != old_slice:
            tick()                # tick each time we cross into a new slice
        time.sleep_ms(20)
    return angle


def land(from_angle):
    # pick a fortune and glide to the middle of its slice
    choice = random.randint(0, len(FORTUNES) - 1)
    target = choice * SLICE_SIZE + SLICE_SIZE // 2
    step = 1 if target > from_angle else -1
    for angle in range(from_angle, target, step):
        set_angle(angle)
        time.sleep_ms(25)
    set_angle(target)
    return choice


set_angle(SLICE_SIZE // 2)   # start pointing at the first slice
print("Press the button to ask the Fortune Teller!")

while True:
    if button.was_pressed():
        print("Spinning...")
        stopped_at = spin()
        choice = land(stopped_at)
        print("The Fortune Teller says:", FORTUNES[choice])
    time.sleep_ms(10)
