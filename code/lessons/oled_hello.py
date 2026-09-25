# Draw text and shapes on a 128x64 SSD1306 OLED screen
from machine import I2C, Pin
import ssd1306

SDA_PIN = 21
SCL_PIN = 22
WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

display.fill(0)                          # clear the screen (all pixels off)
display.rect(0, 0, WIDTH, HEIGHT, 1)     # outline around the edge
display.fill_rect(0, 0, WIDTH, 12, 1)    # solid bar across the top
display.text("CircuitCoder", 16, 2, 0)   # dark text on the bar (colour 0)
display.text("Hello World!", 16, 24, 1)  # lit text (colour 1)
display.line(8, 40, 119, 56, 1)          # diagonal line
display.pixel(64, 60, 1)                 # a single dot

display.show()   # nothing appears until you call show()
