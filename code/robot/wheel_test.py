# First power-on test: spin each wheel forwards for 1 second.
# Lift the robot so its wheels are off the ground before running this!
import time
from machine import Pin, PWM

LEFT_PINS = (16, 17)    # DRV8833 AIN1, AIN2
RIGHT_PINS = (18, 19)   # DRV8833 BIN1, BIN2
TEST_POWER = 60         # percent

left_a = PWM(Pin(LEFT_PINS[0]), freq=20_000, duty_u16=0)
left_b = PWM(Pin(LEFT_PINS[1]), freq=20_000, duty_u16=0)
right_a = PWM(Pin(RIGHT_PINS[0]), freq=20_000, duty_u16=0)
right_b = PWM(Pin(RIGHT_PINS[1]), freq=20_000, duty_u16=0)

duty = int(TEST_POWER * 65535 / 100)

print("LEFT wheel forwards...")
left_a.duty_u16(duty)
time.sleep(1)
left_a.duty_u16(0)
time.sleep(1)

print("RIGHT wheel forwards...")
right_a.duty_u16(duty)
time.sleep(1)
right_a.duty_u16(0)

print("Done. Did the correct wheel spin, in the forward direction?")
