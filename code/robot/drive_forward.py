# The robot's first drive: forwards, stop, backwards
import time
from robot import Robot

robot = Robot()

time.sleep(3)          # time to put the robot on the floor!

robot.forward(60)
time.sleep(1.5)
robot.stop()
time.sleep(0.5)
robot.backward(60)
time.sleep(1.5)
robot.stop()
