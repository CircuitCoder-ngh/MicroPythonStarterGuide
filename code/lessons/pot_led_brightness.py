# Turn the potentiometer to dim or brighten the LED
from machine import ADC, PWM, Pin

POT_PIN = 34
LED_PIN = 27

pot = ADC(Pin(POT_PIN), atten=ADC.ATTN_11DB)
led = PWM(Pin(LED_PIN), freq=1000, duty_u16=0)

while True:
    # Both use the same 0-65535 range, so no maths needed!
    led.duty_u16(pot.read_u16())
