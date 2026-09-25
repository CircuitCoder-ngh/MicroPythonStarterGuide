# Line Follower with memory: if the robot loses the line completely,
# it keeps turning the way it was last turning until it finds it again.
import time
from machine import Pin
from robot import Robot
from button import Button

LEFT_SENSOR_PIN = 34
RIGHT_SENSOR_PIN = 35
BUTTON_PIN = 14
LINE_IS = 1

SPEED = 45
TURN_FAST = 50
TURN_SLOW = -30
LOST_MS = 150    # both sensors off the line for this long = lost

robot = Robot()
button = Button(BUTTON_PIN)
left_sensor = Pin(LEFT_SENSOR_PIN, Pin.IN)
right_sensor = Pin(RIGHT_SENSOR_PIN, Pin.IN)

running = False
last_turn = None                    # "left", "right" or None
last_seen_line = time.ticks_ms()

while True:
    if button.was_pressed():
        running = not running
        last_seen_line = time.ticks_ms()
        if not running:
            robot.stop()

    if not running:
        time.sleep_ms(10)
        continue

    left_on_line = left_sensor.value() == LINE_IS
    right_on_line = right_sensor.value() == LINE_IS
    now = time.ticks_ms()

    if left_on_line or right_on_line:
        last_seen_line = now

    if left_on_line and not right_on_line:
        robot.drive(TURN_SLOW, TURN_FAST)
        last_turn = "left"
    elif right_on_line and not left_on_line:
        robot.drive(TURN_FAST, TURN_SLOW)
        last_turn = "right"
    elif (not left_on_line and time.ticks_diff(now, last_seen_line) > LOST_MS
          and last_turn is not None):
        # lost: search in the direction the line was last heading
        if last_turn == "left":
            robot.spin_left(45)
        else:
            robot.spin_right(45)
    else:
        robot.forward(SPEED)

    time.sleep_ms(5)
