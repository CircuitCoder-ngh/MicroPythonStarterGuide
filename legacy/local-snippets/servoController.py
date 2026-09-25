import machine
import time

BUTTON1_PIN = 14
BUTTON2_PIN = 25
SERVO_PIN = 13

button1 = machine.Pin(BUTTON1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(BUTTON2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50, duty=0)

button1Counter = 0
button2Counter = 0
servo_duty = 0
minduty = 30
maxduty = 140

def th(timer): 
    global button1Counter
    global button2Counter
    if button1Counter == 0:
        button1Counter += 1
    if button2Counter == 0:
        button2Counter += 1

timer = machine.Timer(-1)
timer.init(period=100, mode=machine.Timer.PERIODIC, callback=th)

def updateServo():
    servo.duty(servo_duty)

def checkButtons():
    global button1Counter
    global button2Counter
    global servo_duty
    # decrease servo duty variable by 1 when button1 is pushed,
    if button1Counter > 0:
        if button1.value() == 0:
            button1Counter -= 1
            if servo_duty > minduty: # prevents going below minimum duty
                servo_duty -= 1
                updateServo()
            while button1.value() == 0:
            # if button1 is held down for 0.5 sec,
            # then decrease by 10 every 0.5 second
                time.sleep(0.5)
                if servo_duty > (minduty + 9):
                    servo_duty -= 10
                    updateServo()

    if button2Counter > 0:
        if button2.value() == 0:
            button2Counter -= 1
            if servo_duty < maxduty: # prevents going above maximum duty
                servo_duty += 1
                updateServo()
            while button2.value() == 0:
                # button must be held atleast 0.5 sec before
                # increasing by increments of 10
                time.sleep(0.5) 
                if servo_duty < (maxduty - 9):
                    servo_duty += 10
                    updateServo()

while True:
    checkButtons()

    
