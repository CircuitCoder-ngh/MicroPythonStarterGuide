# Spin one motor forwards, then backwards, through a DRV8833 driver
import time
from machine import Pin

IN1_PIN = 16   # DRV8833 AIN1
IN2_PIN = 17   # DRV8833 AIN2

in1 = Pin(IN1_PIN, Pin.OUT, value=0)
in2 = Pin(IN2_PIN, Pin.OUT, value=0)

print("Forwards")
in1.on()       # IN1 high, IN2 low: current flows one way
in2.off()
time.sleep(2)

print("Stop")
in1.off()      # both low: the motor coasts to a stop
in2.off()
time.sleep(1)

print("Backwards")
in1.off()      # IN1 low, IN2 high: current flows the other way
in2.on()
time.sleep(2)

in2.off()
print("Done")
