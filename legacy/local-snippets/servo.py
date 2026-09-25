import machine
import time

SERVO_PIN = 13 # can be any PWM capable pin

servo_min = 30 # duty level for 0 degrees
servo_max = 140 # duty level for 180 degrees

# initialize the servo motor
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=0, duty=0)

# to set to 0 degrees
servo.duty(servo_min)

# to set to 180 degrees
servo.duty(servo_max)

# to spin continuously
servo.duty(10)

# to turn on, change freq to 50Hz
servo.freq(50)

# prints and increases duty by 1 every 0.5 seconds
for x in range(0,1000,1):
    print(x)
    servo.duty(x)
    time.sleep(0.5)

#to turn off, change freq to 0Hz
servo.freq(0)



