import machine
import time
import ssd1306

# machine pin variables
BUTTON_PIN = 5
POT_PIN1 = 34
POT_PIN2 = 35
SCL_PIN = 22 
SDA_PIN = 21

# button set up
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
buttonCounter = 0

def th(timer): # callback function for the timer (for debouncing buttons)
    global buttonCounter
    if buttonCounter == 0:
        buttonCounter += 1

timer = machine.Timer(-1)
timer.init(period=250, mode=machine.Timer.PERIODIC, callback=th)

# display set up
oled_width = 128
oled_height = 64

i2c = machine.SoftI2C(scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN)) 
display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# potentiometer set up
pot1 = machine.ADC(machine.Pin(POT_PIN1))
pot1.atten(machine.ADC.ATTN_11DB) # full range: 3.3V
pot1.width(machine.ADC.WIDTH_12BIT) # highest resolution, range: 0 to 4095

pot2 = machine.ADC(machine.Pin(POT_PIN2))
pot2.atten(machine.ADC.ATTN_11DB) # based on max voltage going through the pin
pot2.width(machine.ADC.WIDTH_12BIT) # affects resolution of data output

# logic related variables
xy_values = [] 

def update_pots():
# updates cursor's xy position based off potentiometers
# xy_values list consists of mini lists that each have one x and
# one y-coordinate
    global xy_values
    pot1_value = pot1.read()
    pot2_value = pot2.read()
    x_value = int(pot1_value * oled_width / 4095) 
    y_value = int(oled_height - (pot2_value * oled_height / 4095))
    xy_values.append([x_value, y_value])
    if len(xy_values) > 5:
        xy_values.pop(0) # removes old data to save storage space
    
def check_button():
# clears the screen if button is pressed
    global buttonCounter
    if buttonCounter > 0:
        if button.value() == 0:
            buttonCounter -= 1
            display.fill(0)
            display.show()
                
update_pots() 
while True:
    check_button()
    update_pots()
    if xy_values[-2] != xy_values[-1]:
        display.line(xy_values[-2][0], xy_values[-2][1],
                     xy_values[-1][0], xy_values[-1][1], 1)
        display.show()
            
    # (0,0) is the top left on the screen,
    # bottom left would be (0,64)

    

    
    
    
