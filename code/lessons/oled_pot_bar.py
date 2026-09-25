# Show a potentiometer's position as a bar graph on the OLED
from machine import ADC, I2C, Pin
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
pot = ADC(Pin(34), atten=ADC.ATTN_11DB)

while True:
    percent = pot.read_u16() * 100 // 65535
    bar_width = percent * 118 // 100

    display.fill(0)
    display.text("Pot: " + str(percent) + "%", 5, 10, 1)
    display.rect(4, 34, 120, 16, 1)            # empty outline
    display.fill_rect(5, 35, bar_width, 14, 1)  # the filled part
    display.show()
