# A ball that bounces around the OLED screen
import time
from machine import I2C, Pin
import ssd1306

WIDTH = 128
HEIGHT = 64
SIZE = 4   # the ball is a 4x4 square

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

x, y = 10, 20      # position
dx, dy = 2, 1      # speed in pixels per frame

while True:
    x += dx
    y += dy
    # reverse direction when the ball reaches an edge
    if x <= 0 or x >= WIDTH - SIZE:
        dx = -dx
    if y <= 0 or y >= HEIGHT - SIZE:
        dy = -dy

    display.fill(0)
    display.fill_rect(x, y, SIZE, SIZE, 1)
    display.show()
    time.sleep_ms(20)
