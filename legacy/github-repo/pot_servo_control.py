import machine
import time

POT_PIN = 33 # any ADC capable pin
SERVO_PIN = 13 # can be any PWM capable pin

servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50, duty=0)

# potentiometer set up
pot = machine.ADC(machine.Pin(POT_PIN))
pot.atten(machine.ADC.ATTN_11DB) # full range: 3.3V
pot.width(machine.ADC.WIDTH_12BIT) # default, highest resolution, range: 0 to 4095

servo_duty = 0

def updateServo():
    servo.duty(servo_duty)

def updatePot():
    global servo_duty
    pot_value = pot.read() # gets raw output data from potentiometer
    # scales raw pot. output from 4095 to 180
    pot_angle = pot_value * 180 / 4095
    # adjusts variable from 0-180 scale, to 30-140 scale
    servo_duty = int(pot_angle * 11/18) + 30 

while True:
    updatePot()
    updateServo()

