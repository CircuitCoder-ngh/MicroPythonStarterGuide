# Read temperature and humidity from a DHT11 sensor
import time
import dht
from machine import Pin

DHT_PIN = 19

sensor = dht.DHT11(Pin(DHT_PIN))   # use dht.DHT22 for the white DHT22 sensor

while True:
    try:
        sensor.measure()               # ask the sensor for a new reading
        temp_c = sensor.temperature()
        humidity = sensor.humidity()
        temp_f = temp_c * 9 / 5 + 32
        print(f"{temp_c} °C ({temp_f:.1f} °F)   Humidity: {humidity} %")
    except OSError:
        print("Couldn't read the sensor. Check the wiring.")
    time.sleep(2)   # DHT11: at most one reading per second. DHT22: every 2 s
