# robot.py - drive a two-wheeled robot with a DRV8833 motor driver.
#
# Wiring (see the Robot > Build page):
#   Left motor:  DRV8833 AIN1 -> GPIO 16, AIN2 -> GPIO 17
#   Right motor: DRV8833 BIN1 -> GPIO 18, BIN2 -> GPIO 19
#
# Usage:
#   from robot import Robot
#   robot = Robot()
#   robot.forward(60)     # speeds are percentages, 0 to 100
#   robot.spin_left(50)
#   robot.stop()

from machine import Pin, PWM

LEFT_PINS = (16, 17)
RIGHT_PINS = (18, 19)

# If a wheel spins backwards when it should go forwards, set its INVERT to
# True (or swap the motor's two wires on the DRV8833).
LEFT_INVERT = False
RIGHT_INVERT = False

# No two motors are exactly alike. If your robot curves to the right when it
# should go straight, the left motor is faster: set TRIM to a small positive
# number (like 5) to slow it down. Curving left? Use a negative number.
TRIM = 0

# Below about a third of full power, TT motors hum but don't turn. Speed 1
# is mapped to MIN_POWER, so every speed from 1 to 100 actually moves.
MIN_POWER = 35

# 20,000 pulses a second is above human hearing, so the motors don't whine.
PWM_FREQ = 20_000


class Motor:
    def __init__(self, pin_a, pin_b, invert=False, min_power=MIN_POWER):
        self.pwm_a = PWM(Pin(pin_a), freq=PWM_FREQ, duty_u16=0)
        self.pwm_b = PWM(Pin(pin_b), freq=PWM_FREQ, duty_u16=0)
        self.invert = invert
        self.min_power = min_power
        self.speed = 0

    def set_speed(self, speed):
        # speed: -100 (full reverse) to 100 (full forward), 0 = stop
        speed = int(max(-100, min(100, speed)))
        self.speed = speed
        if self.invert:
            speed = -speed

        if speed == 0:
            self.pwm_a.duty_u16(0)   # both inputs low: the motor coasts
            self.pwm_b.duty_u16(0)
            return

        power = self.min_power + (100 - self.min_power) * abs(speed) / 100
        duty = int(power * 65535 / 100)
        if speed > 0:
            self.pwm_a.duty_u16(duty)   # pulse one input...
            self.pwm_b.duty_u16(0)      # ...and hold the other low
        else:
            self.pwm_a.duty_u16(0)
            self.pwm_b.duty_u16(duty)

    def stop(self):
        self.set_speed(0)


class Robot:
    def __init__(self, trim=TRIM):
        self.left = Motor(LEFT_PINS[0], LEFT_PINS[1], LEFT_INVERT)
        self.right = Motor(RIGHT_PINS[0], RIGHT_PINS[1], RIGHT_INVERT)
        self.trim = trim

    def drive(self, left_speed, right_speed):
        # Set each wheel separately: the basis of every other move
        if self.trim > 0:
            left_speed = left_speed * (100 - self.trim) / 100
        elif self.trim < 0:
            right_speed = right_speed * (100 + self.trim) / 100
        self.left.set_speed(left_speed)
        self.right.set_speed(right_speed)

    def forward(self, speed=60):
        self.drive(speed, speed)

    def backward(self, speed=60):
        self.drive(-speed, -speed)

    def spin_left(self, speed=50):
        # wheels turn opposite ways: the robot turns on the spot
        self.drive(-speed, speed)

    def spin_right(self, speed=50):
        self.drive(speed, -speed)

    def stop(self):
        self.drive(0, 0)
