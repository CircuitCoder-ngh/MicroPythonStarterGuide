# Set the ESP32's clock from the internet and print the local time
import time
import ntptime
import secrets
import wifi

wifi.connect()
ntptime.settime()   # sets the clock to UTC (world time)

while True:
    # add your time zone offset to get local time
    local = time.localtime(time.time() + secrets.UTC_OFFSET_HOURS * 3600)
    year, month, day, hour, minute, second = local[0:6]
    print("{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        year, month, day, hour, minute, second))
    time.sleep(1)
