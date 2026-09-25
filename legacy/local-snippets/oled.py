import machine
import time
import ssd1306

# variables for initialization
SCL_PIN = 22 
SDA_PIN = 21
oled_width = 128
oled_height = 64

# initialize screen
i2c = machine.SoftI2C(scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN)) 
display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


# to fill entire screen (turns on all pixels)
display.fill(1)

# to clear screen (turns off all pixels)
display.fill(0)

# to draw rectangular outline from (0,0) to (128,64), color=1
display.rect(0,0,128,64,1)

# to draw a solid rectangle from (0,0) to (128,16), color=1
display.fill_rect(0,0,128,16,1)

# to display text, "Hello World!", at (15,20), color=1
display.text("Hello World!",15,20,1)

# or you could...(lights up screen, and creates black text)
display.fill(1) 
display.text("Hello World!",15,20,0) # color=0

# to draw a line from (0,0) to (127,63), color=1
display.line(0,0,127,63,1)

# changes to screen wont take effect until this command...
display.show() 



