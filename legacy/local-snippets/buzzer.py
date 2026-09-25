import machine
import time

BUZZER_PIN = 26 # can be any PWM capable pin

# initialize buzzer
buzzer = machine.PWM(machine.Pin(BUZZER_PIN), freq=500, duty=0)

# find the frequency you want to use by running a for loop that
# increases the freq and prints it out each iteration
for x in range(100, 1000, 50):
# x starts at 100 and increments by 50 until 1000
    print(x)
    buzzer.freq(x)
    buzzer.duty(500)
    time.sleep(0.4)
    buzzer.duty(0)


