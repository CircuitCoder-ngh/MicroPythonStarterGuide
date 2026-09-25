import machine
import time

POT_PIN = 33 # can be any ADC capable pin

pot = machine.ADC(machine.Pin(POT_PIN))
pot.atten(machine.ADC.ATTN_11DB) # full range: 3.3V
pot.width(machine.ADC.WIDTH_12BIT) # default, highest resolution, range: 0 to 4095

pot.read() # returns current pot value

while True: # prints pot value every 0.5 seconds
    pot_value = pot.read()
    print(pot_value)
    time.sleep(0.5)

