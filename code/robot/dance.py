# A robot dance routine: a list of moves played back in order
import time
from robot import Robot

robot = Robot()

# Each move is (left speed, right speed, milliseconds)
DANCE = [
    (60, 60, 500),      # forwards
    (-60, -60, 500),    # backwards
    (70, -70, 300),     # quick spin right
    (-70, 70, 300),     # quick spin left
    (0, 80, 800),       # swing around the left wheel
    (80, 0, 800),       # swing around the right wheel
    (100, -100, 1200),  # big finish: full spin!
]

time.sleep(3)

for left, right, ms in DANCE:
    robot.drive(left, right)
    time.sleep_ms(ms)

robot.stop()
