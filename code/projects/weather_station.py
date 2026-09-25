# Weather Station: shows the temperature and humidity indoors (DHT11)
# and outdoors (from the internet) on the OLED screen.
# Button A switches between °C and °F.
import time
import dht
import requests
from machine import Pin, I2C
import ssd1306
import wifi
from button import Button

DHT_PIN = 19
BUTTON_PIN = 14   # Button A

# Change these to where you live (search "latitude longitude <your town>")
LATITUDE = 40.71
LONGITUDE = -74.01

INDOOR_EVERY_MS = 2000          # the DHT11 can only measure every ~1-2 s
OUTDOOR_EVERY_MS = 10 * 60000   # ask the internet every 10 minutes

URL = ("https://api.open-meteo.com/v1/forecast"
       "?latitude=" + str(LATITUDE) + "&longitude=" + str(LONGITUDE) +
       "&current=temperature_2m,relative_humidity_2m")

# Step 1: set up each component
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
sensor = dht.DHT11(Pin(DHT_PIN))
button = Button(BUTTON_PIN)

# None means "no reading yet": shown on screen as --
indoor_temp = None
indoor_humidity = None
outdoor_temp = None
outdoor_humidity = None
fahrenheit = False


# Step 2: small functions for each job
def read_indoor():
    global indoor_temp, indoor_humidity
    try:
        sensor.measure()
        indoor_temp = sensor.temperature()
        indoor_humidity = sensor.humidity()
    except OSError:
        print("Couldn't read the DHT11 - check its wiring")


def read_outdoor():
    global outdoor_temp, outdoor_humidity
    try:
        response = requests.get(URL)
        current = response.json()["current"]
        response.close()   # always close, or the ESP32 runs out of memory
        outdoor_temp = current["temperature_2m"]
        outdoor_humidity = current["relative_humidity_2m"]
        print("Outside:", outdoor_temp, "C")
    except Exception as error:
        print("Couldn't get the outdoor weather:", error)
        outdoor_temp = None
        outdoor_humidity = None


def format_temp(celsius):
    if celsius is None:
        return "--"
    if fahrenheit:
        return str(round(celsius * 9 / 5 + 32)) + "F"
    return str(round(celsius)) + "C"


def format_humidity(percent):
    if percent is None:
        return "--"
    return str(round(percent)) + "%"


def draw():
    display.fill(0)
    display.text("Weather Station", 4, 0, 1)
    display.hline(0, 10, 128, 1)
    # left column: inside, right column: outside
    display.text("Inside", 4, 16, 1)
    display.text("Outside", 68, 16, 1)
    display.vline(63, 14, 50, 1)
    display.text(format_temp(indoor_temp), 12, 32, 1)
    display.text(format_temp(outdoor_temp), 76, 32, 1)
    display.text(format_humidity(indoor_humidity), 12, 48, 1)
    display.text(format_humidity(outdoor_humidity), 76, 48, 1)
    display.show()


# Step 3: connect, then update each reading on its own schedule
display.fill(0)
display.text("Connecting...", 4, 28, 1)
display.show()
try:
    wifi.connect()
except RuntimeError as error:
    print(error)   # keep going: indoor readings still work without Wi-Fi

read_indoor()
read_outdoor()
last_indoor = time.ticks_ms()
last_outdoor = time.ticks_ms()
draw()

while True:
    now = time.ticks_ms()

    if button.was_pressed():
        fahrenheit = not fahrenheit
        draw()

    if time.ticks_diff(now, last_indoor) >= INDOOR_EVERY_MS:
        last_indoor = now
        read_indoor()
        draw()

    if time.ticks_diff(now, last_outdoor) >= OUTDOOR_EVERY_MS:
        last_outdoor = now
        read_outdoor()
        draw()

    time.sleep_ms(20)
