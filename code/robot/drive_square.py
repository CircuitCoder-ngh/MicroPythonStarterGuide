# Drive in a square: forwards, turn 90 degrees, four times
import time
from robot import Robot

SPEED = 60
SIDE_MS = 1200     # how long to drive along each side
TURN_MS_90 = 450   # how long a 90-degree spin takes: tune this!

robot = Robot()


def drive_for(left, right, ms):
    robot.drive(left, right)
    time.sleep_ms(ms)
    robot.stop()
    time.sleep_ms(200)   # a short pause makes each move more accurate


time.sleep(3)          # put the robot down

for side in range(4):
    drive_for(SPEED, SPEED, SIDE_MS)        # straight
    drive_for(SPEED, -SPEED, TURN_MS_90)    # spin right

print("Square complete!")
