import machine
import time

BUTTON1_PIN = 14
BUTTON2_PIN = 25
SERVO_PIN = 13

button1 = machine.Pin(BUTTON1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(BUTTON2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50, duty=0)

buttonCounter = 0
servo_duty = 30
minduty = 30
maxduty = 140

def th(timer): 
    global buttonCounter
    if buttonCounter == 0:
        buttonCounter += 1

timer = machine.Timer(-1)
timer.init(period=250, mode=machine.Timer.PERIODIC, callback=th)

def updateServo():
    servo.duty(servo_duty)

def checkButtons():
    global buttonCounter
    global servo_duty
    if buttonCounter > 0:
        # decrease servo duty by 1 when button1 is pressed
        if button1.value() == 0:
            buttonCounter -= 1
            if servo_duty > minduty: # prevents going below minimum duty
                servo_duty -= 1 
                updateServo()
        # increase servo duty by 1 when button2 is pressed    
        else if button2.value() == 0:
            buttonCounter -= 1
            if servo_duty < maxduty: # prevents going above maximum duty
                servo_duty += 1
                updateServo()
            

while True:
    checkButtons()

    
