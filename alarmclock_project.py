import machine
import time
import network # for connecting to Wi-Fi
import urequests # for GET/POST requests to APIs
import ssd1306 # for controlling the OLED screen

SSID = "Pixel_9396"
PASSWORD = "holdmynuts"
URL = "http://worldtimeapi.org/api/ip" # gets time based off your IP address

BUZZER_PIN = 26
BUTTON1_PIN = 27
BUTTON2_PIN = 14
BUTTON3_PIN = 12
SCL_PIN = 22 
SDA_PIN = 21
oled_width = 128
oled_height = 64

button1 = machine.Pin(BUTTON1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(BUTTON2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button3 = machine.Pin(BUTTON3_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

buzzer = machine.PWM(machine.Pin(BUZZER_PIN), freq=500, duty=0)

i2c = machine.SoftI2C(scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN)) 
display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# setting defaults for global variables
# (code would crash otherwise)
buttonCounter = 0
page = 1 # for switching pages
date = 0
localtime = 0
hours = 0
minutes = 0
alarmOn = False # alarm is off by default
alarmHours = 8 # sets default alarm time to 8:00am
alarmMinutes = 0
stopMinutes = 0 # for stop-clock
stopSeconds = 0
stopMSeconds = 0
timerHours = 0 # for timer
timerMinutes = 0
timerSeconds = 0

# for debouncing buttons
def th(timer): 
    global buttonCounter
    if buttonCounter == 0:
        buttonCounter += 1

timer = machine.Timer(-1)
timer.init(period=500, mode=machine.Timer.PERIODIC, callback=th)

# connect ESP32 to Wi-Fi
def connectWifi():
    api_if = network.WLAN(network.AP_IF)
    api_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to wifi...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Network config: ' + str(sta_if.ifconfig()))

# updates date and localtime variables from internet API
def updateTime():
    global date
    global localtime
    global hours
    global minutes
    try:
        response = urequests.get(URL)
        # print(response.text) # returns string of all content
        text = response.json() # returns dictionary of content items
        date = text["datetime"][0:10]
        localtime = text["datetime"][11:19]
        hours = int(text["datetime"][11:13])
        minutes = int(text["datetime"][14:16])
        print(date + ' --- ' + localtime)
    except:
        print('Read data request failed')
        print(response.status_code) # 200-300 is good, 400+ is bad

# checks buttons and executes the desired function
def checkButtons():
# two buttons for scrolling, one for selecting
# selecting time turns alarm on/off
# selecting alarm allows changing alarm
# selecting timer allows editing, then starts
# selecting stopclock begins
    global buttonCounter
    if buttonCounter > 0:
        if button1.value() == 0:
            buttonCounter -= 1
            scroll_left()
        elif button2.value() == 0:
            buttonCounter -= 1
            select()
        elif button3.value() == 0:
            buttonCounter -= 1
            scroll_right()
            
def scroll_left():
    global page
    page -= 1
    if page == 0:
        page = 4
        
def scroll_right():
    global page
    page += 1
    if page == 5:
        page = 1
    
def select():
    # page 1 = datetime and alarm
    # page 2 = edit alarm
    # page 3 = stop-clock
    # page 4 = timer
    if page == 1:
        alarmSwitch() # turns alarm on/off
    elif page == 2:
        changeAlarm() # edit alarm time
    elif page == 3:
        stopclockSwitch() # turns stopclock on/off
    else:
        timer() # edit then activate timer
        
def alarmSwitch():
    global alarmOn
    if alarmOn == True:
        alarmOn = False
    else:
        alarmOn = True

def changeAlarm():
    global buttonCounter
    global alarmHours
    global alarmMinutes
    
    while True: # remain in this loop until button 2 pushed
        updateDisplay()
        # underline part being edited
        display.line(15,30,25,30,1) # draws line from (15,30) to (20,30)
        display.show()
        if buttonCounter > 0: 
            if button1.value() == 0: # button 1 decreases alarm hour
                buttonCounter -= 1
                if alarmHours > 0:
                    alarmHours -= 1
            elif button2.value() == 0: # button 2 breaks out of loop
                buttonCounter -= 1
                break
            elif button3.value() == 0: # button 3 increases alarm hour
                buttonCounter -= 1
                if alarmHours < 24:
                    alarmHours += 1
        
    while True:
        updateDisplay()
        display.line(30,30,40,30,1) # draws line from (15,30) to (20,30)
        display.show()
        if buttonCounter > 0: 
            if button1.value() == 0: # button 1 decreases alarm minutes
                buttonCounter -= 1
                if alarmMinutes > 0:
                    alarmMinutes -= 1
            elif button2.value() == 0: # button 2 breaks out of loop
                buttonCounter -= 1
                break
            elif button3.value() == 0: # button 3 increases alarm minutes
                buttonCounter -= 1
                if alarmMinutes < 59:
                    alarmMinutes += 1
            

def stopclockSwitch():
    global buttonCounter
    global stopMinutes
    global stopSeconds
    global stopMSeconds
    stopMinutes = 0
    stopSeconds = 0
    while True: # remain in stop-clock until button 2 pushed
        updateDisplay()
        stopMSeconds += 1
        if stopMSeconds == 10:
            stopMSeconds -= 10
            stopSeconds += 1
        if stopSeconds == 60:
            stopSeconds -= 60
            stopMinutes += 1
        time.sleep(0.1)
        if buttonCounter > 0: # button 2 breaks out of loop
            if button2.value() == 0:
                buttonCounter -= 1
                break
    
def timer():
    global buttonCounter
    global timerHours
    global timerMinutes
    global timerSeconds
    timerHours = 0
    timerMinutes = 0
    timerSeconds = 0
    while True: # edit timer hours
        display.line(15,30,18,30,1)
        updateDisplay()
        if buttonCounter > 0: 
            if button1.value() == 0: # button 1 decreases timer hours
                buttonCounter -= 1
                if timerHours > 0:
                    timerHours -= 1
         # button 2 breaks out of loop
            elif button2.value() == 0:
                buttonCounter -= 1
                break
         # button 3 increases timer hours
            elif button3.value() == 0:
                buttonCounter -= 1
                if timerHours < 12:
                    timerHours += 1
    while True: # edit timer minutes
        display.line(20,30,23,30,1)
        updateDisplay()
        if buttonCounter > 0: 
            if button1.value() == 0: # button 1 decreases timer minutes
                buttonCounter -= 1
                if timerMinutes > 0:
                    timerMinutes -= 1
            elif button2.value() == 0: # button 2 breaks out of loop
                buttonCounter -= 1
                break
            elif button3.value() == 0: # button 3 increases timer minutes
                buttonCounter -= 1
                if timerMinutes < 59:
                    timerMinutes += 1

    while True: # edit timer seconds
        display.line(25,30,29,30,1)
        updateDisplay()
        if buttonCounter > 0: 
            if button1.value() == 0: # button 1 decreases timer seconds
                buttonCounter -= 1
                if timerSeconds > 0:
                    timerSeconds -= 1
            elif button2.value() == 0: # button 2 breaks out of loop
                buttonCounter -= 1
                break
            elif button3.value() == 0: # button 3 increases timer hours
                buttonCounter -= 1
                if timerSeconds < 59:
                    timerSeconds += 1

    while True: # timer counts down, exit with any button
        updateDisplay()
        if timerSeconds > 0:
            timerSeconds -= 1
        else:
            if timerMinutes > 0:
                timerMinutes -= 1
                timerSeconds = 59
            else:
                if timerHours > 0:
                    timerHours -= 1
                    timerMinutes = 59
                else:
                    # set off buzzer for 1 second
                    buzzer.duty(500)
                    time.sleep(1)
                    buzzer.duty(0)
                    break        
        if buttonCounter > 0 :
            if button1.value() == 0:
                buttonCounter -= 1
                break
            elif button2.value() == 0:
                buttonCounter -= 1
                break
            elif button3.value() == 0:
                buttonCounter -= 1
                break
        time.sleep(1)

# updates display based on current page number (4 pages)
def updateDisplay():
    if page == 1:
        # print date and time on screen
        # print alarm time if active
        display.text(date,15,5,1)
        display.text("Time: " + localtime,15,20,1)
        if alarmOn: # this is equivalent to "if alarmOn == True:"
            display.text("Alarm Active",15,35,1)
            display.line(15,45,110,45,1)
            display.text(formatData(alarmHours) + ":" +
                         formatData(alarmMinutes),25,50,1)
    elif page == 2:
        # print "editing alarm", alarm time
        display.text("Edit Alarm",15,5,1)
        display.text(formatData(alarmHours) + ":" +
                     formatData(alarmMinutes),15,20,1)
    elif page == 3:
        # print stop min, sec
        display.text("Stopclock",15,5,1)
        display.text(formatData(stopMinutes) + ":" +
                     formatData(stopSeconds) + ":" +
                     formatData(stopMSeconds),15,20,1)
    elif page == 4:
        # print timer hours, min, sec
        display.text("Timer",15,5,1)
        
        display.text(formatData(timerHours) + ":" +
                     formatData(timerMinutes) + ":" +
                     formatData(timerSeconds),15,20,1)
    display.show()
    display.fill(0)

# formats the integer parameter into a string 
def formatData(number):
    if number < 10:
        number = "0" + str(number)
    else:
        number = str(number)

    return number

def alarm():
    if alarmOn == True:
        if hours == alarmHours:
            if minutes == alarmMinutes:
                buzzer.duty(500)
                time.sleep(1)
                buzzer.duty(0)
    
connectWifi()


while True:
    if page == 1:
        updateTime()
        alarm()
    checkButtons()
    updateDisplay()
    

            
