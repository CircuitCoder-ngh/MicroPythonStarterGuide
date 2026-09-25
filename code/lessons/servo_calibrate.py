# Find the pulse lengths your servo really uses for 0 and 180 degrees.
# Watch the horn: note the value where it stops moving at each end.
import time
from machine import PWM, Pin

SERVO_PIN = 13

servo = PWM(Pin(SERVO_PIN), freq=50, duty_u16=0)

# try pulses from 0.4 ms to 2.6 ms in 0.05 ms steps
for pulse_us in range(400, 2601, 50):
    print("pulse:", pulse_us, "us  ->  use", pulse_us * 1000, "ns")
    servo.duty_ns(pulse_us * 1000)
    time.sleep(0.5)

servo.duty_u16(0)
