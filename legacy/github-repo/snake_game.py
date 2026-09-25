import time
import machine
import ssd1306
import random

# config variables
DISPLAY_SCL_PIN = 22
DISPLAY_SDA_PIN = 21
BUTTON1_PIN = 27
BUTTON2_PIN = 12
oled_width = 128
oled_height = 64

# initialize buttons
button1 = machine.Pin(BUTTON1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(BUTTON2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# initialize screen
i2c = machine.SoftI2C(scl=machine.Pin(DISPLAY_SCL_PIN),
                  sda=machine.Pin(DISPLAY_SDA_PIN))
display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c) 

# global variables
buttonCounter = 0
xy_list = [(64,32)] # first position is middle of screen
direction = 'up'
length = 1
running = False
apple_position = 0

def th(timer):
    # for this program we can use one buttonCounter for both buttons
    # since the user can only turn one direction at a time anyway
    global buttonCounter
    if buttonCounter == 0:
        buttonCounter += 1

timer = machine.Timer(-1)
timer.init(period=400, mode=machine.Timer.PERIODIC, callback=th)

# creates new position coordinates using direction and last position
def update_position():
    global xy_list
    last_xy = xy_list[-1]
    if direction == 'left':
        new_xy = (last_xy[0] + 1, last_xy[1])
    elif direction == 'right':
        new_xy = (last_xy[0] - 1, last_xy[1])
    elif direction == 'up':
        new_xy = (last_xy[0], last_xy[1] + 1)
    elif direction == 'down':
        new_xy = (last_xy[0], last_xy[1] - 1)

    if new_xy in xy_list: # game over if you hit yourself
        game_over()
    else:
        xy_list.append(new_xy)

# generates apple coordinates
def generate_apple():
    global apple_position
    x = random.randint(1,127)
    y = random.randint(16,63)
    apple_position = (x,y)

# checks if position == apple position, and if out of bounds
def apple_check():
    global length
    global xy_list
    last_xy = xy_list[-1]
    if last_xy == apple_position:
        length += 1
        generate_apple()
        
    elif last_xy[0] <= 0:
        game_over()
    elif last_xy[0] >= 128:
        game_over()
    elif last_xy[1] <= 15:
        game_over()
    elif last_xy[1] >= 64:
        game_over()
            
    if len(xy_list) > length:
        xy_list.pop(0)

# if game is not running, check buttons to start game...otherwise,
# button1 turns user left (relative to current direction),
# and button2 turns user right (relative to current direction)
def check_buttons():
    global buttonCounter
    global direction
    global running
    if running == False:
        if buttonCounter > 0:
            if button1.value() == 0:
                buttonCounter -= 1
                running = True
            elif button2.value() == 0:
                buttonCounter -= 1
                running = True
                
    elif direction == 'left':
        if buttonCounter > 0:
            if button1.value() == 0:
                buttonCounter -= 1
                direction = 'down'    
            elif button2.value() == 0:
                buttonCounter -= 1
                direction = 'up'

    elif direction == 'right':
        if buttonCounter > 0:
            if button1.value() == 0:
                buttonCounter -= 1
                direction = 'up'    
            elif button2.value() == 0:
                buttonCounter -= 1
                direction = 'down'

    elif direction == 'up':
        if buttonCounter > 0:
            if button1.value() == 0:
                buttonCounter -= 1
                direction = 'left'
            elif button2.value() == 0:
                buttonCounter -= 1
                direction = 'right'

    elif direction == 'down':
        if buttonCounter > 0:
            if button1.value() == 0:
                buttonCounter -= 1
                direction = 'right'  
            elif button2.value() == 0:
                buttonCounter -= 1
                direction = 'left'

# updates display to show current position of 'snake'
def update_display():
    display.fill(0)
    for i in range(0, len(xy_list)):
        point = xy_list[i]
        display.pixel(point[0],point[1],1)
    display.rect(0,16,128,48,1)
    display.pixel(apple_position[0],apple_position[1],1)
    display.text('Score: ' + str(length - 1), 12,4,1)
    if running == False:
        display.text('Click button',12,25,1)
        display.text('to begin',15,35,1)
    display.show()

# displays final score and resets variables for next game
def game_over():
    global running
    if running == True:
        running = False
        display.fill_rect(12,20,104,40,1)
        display.text('Game Over: ' + str(length -1),15,30,0)
        display.show()
        reset_variables()
        time.sleep(2)

# reset all starting variables
def reset_variables():
    global xy_list
    global direction
    global length
    xy_list = [(64,32)] 
    direction = 'up'
    length = 1
    generate_apple()
    

while True:
    reset_variables() # ensures that you get a randomly generated
    # apple position with every new game you start
    
    while running == True:
        check_buttons()
        update_position()
        apple_check()
        update_display()

    while running == False:
        check_buttons()
        update_display()

    
