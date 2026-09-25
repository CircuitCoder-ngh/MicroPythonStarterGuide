# Etch-a-Sketch: draw on the OLED screen with two potentiometers.
# Pot 1 moves left/right, Pot 2 moves up/down.
# Button A lifts or lowers the pen, Button B clears the screen.
import time
from machine import Pin, ADC, I2C
import ssd1306
from button import Button

POT_X_PIN = 34    # Potentiometer 1
POT_Y_PIN = 35    # Potentiometer 2
PEN_BUTTON_PIN = 14    # Button A
CLEAR_BUTTON_PIN = 25  # Button B
SDA_PIN = 21
SCL_PIN = 22

WIDTH = 128
HEIGHT = 64

# ---- set up the parts ----
pot_x = ADC(Pin(POT_X_PIN), atten=ADC.ATTN_11DB)
pot_y = ADC(Pin(POT_Y_PIN), atten=ADC.ATTN_11DB)
pen_button = Button(PEN_BUTTON_PIN)
clear_button = Button(CLEAR_BUTTON_PIN)
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

pen_down = True
cursor_shown = False    # is the blinking cursor currently drawn?
cursor_under = 0        # the pixel that was under the cursor
last_blink = time.ticks_ms()


def read_smooth(pot):
    # average 16 readings to stop the line from jittering
    total = 0
    for _ in range(16):
        total += pot.read_u16()
    return total // 16


def read_position():
    x = read_smooth(pot_x) * (WIDTH - 1) // 65535
    # (0, 0) is the TOP left of the screen, so flip y:
    # turning the dial up moves the pen up
    y = (HEIGHT - 1) - read_smooth(pot_y) * (HEIGHT - 1) // 65535
    return x, y


def show_cursor(x, y):
    # draw the cursor as the opposite of whatever pixel is underneath
    global cursor_shown, cursor_under
    cursor_under = display.pixel(x, y)
    display.pixel(x, y, 1 - cursor_under)
    cursor_shown = True


def hide_cursor(x, y):
    # put back the pixel that was under the cursor
    global cursor_shown
    if cursor_shown:
        display.pixel(x, y, cursor_under)
        cursor_shown = False


def blink_cursor(x, y):
    # while the pen is up, flash one pixel so you can see where you are
    global last_blink
    if time.ticks_diff(time.ticks_ms(), last_blink) > 300:
        last_blink = time.ticks_ms()
        if cursor_shown:
            hide_cursor(x, y)
        else:
            show_cursor(x, y)
        display.show()


display.fill(0)
display.show()
last_x, last_y = read_position()

while True:
    if clear_button.was_pressed():
        display.fill(0)
        display.show()
        cursor_shown = False

    if pen_button.was_pressed():
        hide_cursor(last_x, last_y)
        pen_down = not pen_down
        print("Pen down" if pen_down else "Pen up")

    x, y = read_position()

    if pen_down:
        if (x, y) != (last_x, last_y):
            display.line(last_x, last_y, x, y, 1)
            display.show()
    else:
        if (x, y) != (last_x, last_y):
            hide_cursor(last_x, last_y)   # the cursor moves with the dials
            display.show()
        blink_cursor(x, y)

    last_x, last_y = x, y
    time.sleep_ms(5)
