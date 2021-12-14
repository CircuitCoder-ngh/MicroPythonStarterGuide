import machine
import time

buttonCounter = 0
playing = False

BUZZER_PIN = 26
BUTTON_PIN = 14
POT_PIN = 33

# you can set the frequency to anything between 10 and 12000
buzzer = machine.PWM(machine.Pin(BUZZER_PIN), freq=500, duty=0)
max_duty = 1000

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

pot = machine.ADC(machine.Pin(POT_PIN))
pot.atten(machine.ADC.ATTN_11DB) # full range: 3.3v
pot.width(machine.ADC.WIDTH_12BIT) #range: 0 to 4095

def th(timer): # callback function for the timer
    global buttonCounter
    if buttonCounter == 0:
        buttonCounter += 1
        
timer = machine.Timer(-1)
# timer executes th() function every 250ms
timer.init(period=250, mode=machine.Timer.PERIODIC, callback=th) 

def button_pressed():
    global playing
    if playing == True:
        buzzer.duty(0)
        playing = False
    else:
        playing = True

def adjust_volume():
    pot_value = pot.read()
    duty = int(max_duty * pot_value / 4095)
    buzzer.duty(duty)

while True:
    if buttonCounter > 0:
        if button.value() == 0:
            button_pressed()
            buttonCounter -= 1
    
    if playing == True:
        adjust_volume()

