# Sonar Radar: a servo sweeps an ultrasonic sensor back and forth,
# and the OLED draws what it "sees" like a radar screen.
import math
import time
from machine import Pin, PWM, I2C
import ssd1306
from distance import DistanceSensor

SERVO_PIN = 13
SERVO_MIN_NS = 500_000     # pulse for 0°   (see the Servo lesson)
SERVO_MAX_NS = 2_500_000   # pulse for 180°

RANGE_CM = 100    # objects further away than this aren't drawn
STEP = 3          # degrees to move between measurements
SETTLE_MS = 40    # time for the servo to reach each new angle

# The radar is a half circle: its centre is at the middle of the
# bottom edge of the screen, and its radius fills the screen height.
CENTRE_X = 64
CENTRE_Y = 63
RADIUS = 60

# Step 1: set up each component
servo = PWM(Pin(SERVO_PIN), freq=50, duty_u16=0)
sensor = DistanceSensor(trigger_pin=5, echo_pin=39, max_cm=RANGE_CM + 20)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# One entry per angle we measure: the distance seen there, or None
blips = {}


# Step 2: small functions for each job
def set_angle(angle):
    pulse = SERVO_MIN_NS + (SERVO_MAX_NS - SERVO_MIN_NS) * angle // 180
    servo.duty_ns(pulse)


def polar_to_screen(angle, length):
    # Convert "angle and distance from the centre" into x, y pixels.
    # 0° points right, 90° points straight up, 180° points left.
    radians = math.radians(angle)
    x = CENTRE_X + int(length * math.cos(radians))
    y = CENTRE_Y - int(length * math.sin(radians))
    return x, y


def draw_grid():
    # Three range rings (a third, two thirds and full range)...
    for ring in (RADIUS // 3, 2 * RADIUS // 3, RADIUS):
        for angle in range(0, 181, 6):
            x, y = polar_to_screen(angle, ring)
            display.pixel(x, y, 1)
    # ...and a line along the bottom
    display.hline(CENTRE_X - RADIUS, CENTRE_Y, 2 * RADIUS + 1, 1)


def draw(sweep_angle):
    display.fill(0)
    draw_grid()
    # the sweep line
    x, y = polar_to_screen(sweep_angle, RADIUS)
    display.line(CENTRE_X, CENTRE_Y, x, y, 1)
    # a small filled square for every echo we've seen
    for angle, cm in blips.items():
        bx, by = polar_to_screen(angle, cm * RADIUS // RANGE_CM)
        display.fill_rect(bx - 1, by - 1, 3, 3, 1)
    # the latest distance, in the top-left corner
    cm = blips.get(sweep_angle)
    display.text("--" if cm is None else str(cm) + "cm", 0, 0, 1)
    display.show()


def scan(angle):
    set_angle(angle)
    time.sleep_ms(SETTLE_MS)
    cm = sensor.distance_cm()
    # Replace whatever was at this angle last time: that's what
    # clears old blips as the sweep passes over them.
    if cm is not None and cm <= RANGE_CM:
        blips[angle] = int(cm)
    elif angle in blips:
        del blips[angle]
    print(angle, "degrees:", cm, "cm")
    draw(angle)


# Step 3: sweep left to right, then right to left, forever
while True:
    for angle in range(0, 181, STEP):
        scan(angle)
    for angle in range(180, -1, -STEP):
        scan(angle)
