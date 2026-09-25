# Motion Alert: sends a notification to your phone when the
# motion sensor spots someone, using the free ntfy.sh service.
import time
import network
import requests
from machine import Pin
import wifi
import secrets

PIR_PIN = 33
LED_PIN = 27
COOLDOWN_S = 60   # wait at least this long between notifications

pir = Pin(PIR_PIN, Pin.IN)   # the sensor drives the pin itself: no pull-up
led = Pin(LED_PIN, Pin.OUT)
URL = "https://ntfy.sh/" + secrets.NTFY_TOPIC


def send_alert():
    try:
        response = requests.post(
            URL,
            data="Motion detected!",
            headers={"Title": "CircuitCoder Motion Alert", "Tags": "rotating_light"},
        )
        print("Alert sent, status", response.status_code)
        response.close()   # always close, or the ESP32 runs out of memory
        return True
    except Exception as error:
        print("Couldn't send the alert:", error)
        return False


def check_wifi():
    # reconnect if the Wi-Fi dropped out
    if not network.WLAN(network.WLAN.IF_STA).isconnected():
        print("Wi-Fi lost, reconnecting...")
        try:
            wifi.connect()
        except RuntimeError as error:
            print(error)


wifi.connect()
print("Warming up the sensor (about 30 seconds)...")
time.sleep(30)
print("Watching for motion!")

last_alert = None
was_moving = False

while True:
    moving = pir.value() == 1
    led.value(moving)

    # only act at the START of a movement, not the whole time it lasts
    if moving and not was_moving:
        print("Motion!")
        cooled_down = (last_alert is None or
                       time.time() - last_alert > COOLDOWN_S)
        if cooled_down:
            check_wifi()
            if send_alert():
                last_alert = time.time()
        else:
            print("(still cooling down, no alert sent)")

    was_moving = moving
    time.sleep_ms(100)
