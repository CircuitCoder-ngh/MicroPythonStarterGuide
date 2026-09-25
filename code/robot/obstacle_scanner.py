# Obstacle Avoider, level 2: when blocked, look left and right with a
# servo-mounted sensor and turn towards the more open side.
# Press Button A to start and stop.
import time
from machine import Pin, PWM
from robot import Robot
from button import Button
from distance import DistanceSensor

BUTTON_PIN = 14
SERVO_PIN = 13
CRUISE_SPEED = 55
TOO_CLOSE_CM = 25
FAR_AWAY_CM = 250     # what "nothing in range" counts as

SERVO_MIN_NS = 500_000
SERVO_MAX_NS = 2_500_000
LOOK_AHEAD, LOOK_LEFT, LOOK_RIGHT = 90, 160, 20   # servo angles
TURN_MS_90 = 450

robot = Robot()
button = Button(BUTTON_PIN)
sensor = DistanceSensor(trigger_pin=5, echo_pin=39)
servo = PWM(Pin(SERVO_PIN), freq=50, duty_u16=0)


def set_angle(angle):
    angle = max(0, min(180, angle))
    servo.duty_ns(SERVO_MIN_NS + (SERVO_MAX_NS - SERVO_MIN_NS) * angle // 180)


def look(angle):
    # point the sensor, give the servo time to get there, then measure
    set_angle(angle)
    time.sleep_ms(350)
    distance = sensor.distance_cm()
    if distance is None:
        return FAR_AWAY_CM
    return distance


def choose_new_direction():
    robot.stop()
    robot.backward(45)
    time.sleep_ms(250)
    robot.stop()

    left = look(LOOK_LEFT)
    right = look(LOOK_RIGHT)
    look(LOOK_AHEAD)
    print("Left:", left, "cm  Right:", right, "cm")

    if left < TOO_CLOSE_CM and right < TOO_CLOSE_CM:
        robot.spin_right(55)            # boxed in: turn around
        time.sleep_ms(TURN_MS_90 * 2)
    elif left > right:
        robot.spin_left(55)
        time.sleep_ms(TURN_MS_90)
    else:
        robot.spin_right(55)
        time.sleep_ms(TURN_MS_90)
    robot.stop()


set_angle(LOOK_AHEAD)
running = False
print("Press Button A to start")

while True:
    if button.was_pressed():
        running = not running
        print("Go!" if running else "Stopped")
        if not running:
            robot.stop()

    if not running:
        time.sleep_ms(10)
        continue

    distance = sensor.distance_cm()
    if distance is not None and distance < TOO_CLOSE_CM:
        choose_new_direction()
    else:
        robot.forward(CRUISE_SPEED)
