# Chirp the buzzer and flash the LED each time motion starts
import time
from machine import PWM, Pin

pir = Pin(33, Pin.IN)
led = Pin(27, Pin.OUT)
buzzer = PWM(Pin(26), freq=1500, duty_u16=0)


def chirp():
    for i in range(3):
        led.on()
        buzzer.duty_u16(32768)
        time.sleep_ms(100)
        led.off()
        buzzer.duty_u16(0)
        time.sleep_ms(100)


last_value = pir.value()
while True:
    value = pir.value()
    if value == 1 and last_value == 0:   # motion just started
        chirp()
    last_value = value
    time.sleep_ms(50)
