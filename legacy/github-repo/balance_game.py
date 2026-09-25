import machine
import time

SERVO1_PIN = 12
SERVO2_PIN = 13
SERVO3_PIN = 27
POT1_PIN = 34 # can be any ADC capable pin
POT2_PIN = 35

servo_min = 30 # duty level for 0 degrees
servo_max = 140 # duty level for 180 degrees

servo1 = machine.PWM(machine.Pin(SERVO1_PIN), freq=0, duty=0) # left base servo
servo2 = machine.PWM(machine.Pin(SERVO2_PIN), freq=0, duty=0) # right base servo
servo3 = machine.PWM(machine.Pin(SERVO3_PIN), freq=0, duty=0) # top servo

pot1 = machine.ADC(machine.Pin(POT1_PIN)) # controls both base servos
pot1.atten(machine.ADC.ATTN_11DB) # full range: 3.3V
pot1.width(machine.ADC.WIDTH_12BIT) # default, highest resolution, range: 0 to 4095

pot2 = machine.ADC(machine.Pin(POT2_PIN)) # controls the top servo
pot2.atten(machine.ADC.ATTN_11DB)
pot2.width(machine.ADC.WIDTH_12BIT) 

# turns the servos on
servo1.freq(50)
servo2.freq(50)
servo3.freq(50)

# continuously update servos' position to match potentiometers
while True:
    # variables for base motors
    pot1_angle = pot1.read() * 180 / 4095 # scales raw pot. output from 4095 to 180
    servo1_duty = (pot1_angle * 11/18) + 30 # adjusts variable from 0-180 scale, to 30-140 scale
    servo2_duty = 180 - servo1_duty # mirrors the angle of servo 1
    
    # variables for top motor
    pot2_angle = pot2.read() * 180 / 4095
    servo3_duty = (pot2_angle * 11/18) + 30
    
    # sets all the servos to the desired position
    servo1.duty(int(servo1_duty))
    servo2.duty(int(servo2_duty))
    servo3.duty(int(servo3_duty))
