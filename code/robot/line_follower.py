# Line Follower: steer along a black tape line with two sensors.
# Press Button A to start and stop.
import time
from machine import Pin
from robot import Robot
from button import Button

LEFT_SENSOR_PIN = 34
RIGHT_SENSOR_PIN = 35
BUTTON_PIN = 14
LINE_IS = 1          # sensor value over the black line (0 on some modules)

SPEED = 45           # straight-ahead speed
TURN_FAST = 50       # outside wheel while turning
TURN_SLOW = -30      # inside wheel while turning (negative = backwards)

robot = Robot()
button = Button(BUTTON_PIN)
left_sensor = Pin(LEFT_SENSOR_PIN, Pin.IN)
right_sensor = Pin(RIGHT_SENSOR_PIN, Pin.IN)

running = False
print("Put the robot on the line, then press Button A")

while True:
    if button.was_pressed():
        running = not running
        print("Go!" if running else "Stopped")
        if not running:
            robot.stop()

    if not running:
        time.sleep_ms(10)
        continue

    left_on_line = left_sensor.value() == LINE_IS
    right_on_line = right_sensor.value() == LINE_IS

    if left_on_line and not right_on_line:
        robot.drive(TURN_SLOW, TURN_FAST)    # line is drifting left: turn left
    elif right_on_line and not left_on_line:
        robot.drive(TURN_FAST, TURN_SLOW)    # line is drifting right: turn right
    else:
        robot.forward(SPEED)   # line between the sensors (or a crossing)

    time.sleep_ms(5)
