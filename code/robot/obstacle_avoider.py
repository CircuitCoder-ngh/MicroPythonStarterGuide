# Obstacle Avoider: drive around on your own, dodging anything in the way.
# Press Button A to start and stop.
import random
import time
from machine import Pin, PWM
from robot import Robot
from button import Button
from distance import DistanceSensor

BUTTON_PIN = 14
BUZZER_PIN = 26
CRUISE_SPEED = 55     # percent
TOO_CLOSE_CM = 20     # react to anything nearer than this

robot = Robot()
button = Button(BUTTON_PIN)
sensor = DistanceSensor(trigger_pin=5, echo_pin=39)
buzzer = PWM(Pin(BUZZER_PIN), freq=2000, duty_u16=0)


def chirp():
    buzzer.freq(2000)
    buzzer.duty_u16(32768)
    time.sleep_ms(60)
    buzzer.duty_u16(0)


def avoid():
    # stop, back away, then turn a random direction for a random time
    robot.stop()
    chirp()
    robot.backward(50)
    time.sleep_ms(400)
    turn_ms = random.randint(300, 700)
    if random.randint(0, 1) == 0:
        robot.spin_left(55)
    else:
        robot.spin_right(55)
    time.sleep_ms(turn_ms)
    robot.stop()


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

    distance = sensor.distance_cm()     # None means nothing in range
    if distance is not None and distance < TOO_CLOSE_CM:
        print("Obstacle at", distance, "cm")
        avoid()
    else:
        robot.forward(CRUISE_SPEED)
