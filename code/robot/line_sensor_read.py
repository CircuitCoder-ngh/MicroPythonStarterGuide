# Print what the two line sensors see
import time
from machine import Pin

LEFT_SENSOR_PIN = 34
RIGHT_SENSOR_PIN = 35

# The value a sensor gives when it's over the black line. Most TCRT5000
# modules give 1 over black; if yours is the other way round, change to 0.
LINE_IS = 1

left_sensor = Pin(LEFT_SENSOR_PIN, Pin.IN)    # the module has its own
right_sensor = Pin(RIGHT_SENSOR_PIN, Pin.IN)  # pull-up resistor


def describe(sensor):
    if sensor.value() == LINE_IS:
        return "LINE "
    return "floor"


while True:
    print("Left:", describe(left_sensor), "  Right:", describe(right_sensor))
    time.sleep_ms(200)
