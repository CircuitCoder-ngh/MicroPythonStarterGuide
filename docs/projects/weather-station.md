# Project: Weather Station

<img src="../../assets/img/icons/temperature.svg" alt="" class="cc-icon">

Is it warmer inside or out? Your weather station knows. A DHT11 sensor
measures the temperature and humidity in your room, the ESP32 fetches the
weather outside from the internet, and the OLED shows them side by side.

## Objective

- Show **indoor** temperature and humidity from the DHT11, updated every
  2 seconds.
- Show **outdoor** temperature and humidity from the free
  [Open-Meteo](https://open-meteo.com) weather API, updated every 10 minutes.
- **Button A** switches between **°C** and **°F**.
- If something goes wrong (no Wi-Fi, sensor unplugged), show `--` instead of
  crashing.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × DHT11 temperature & humidity module
- [x] 1 × SSD1306 OLED screen (128 × 64, I2C)
- [x] 1 × push button
- [x] Jumper wires
- [x] A 2.4 GHz Wi-Fi network
</div>

!!! note "Before you start"
    This project uses what you learned in [Temperature & Humidity](../components/temperature.md),
    [OLED Screens](../components/oled.md), [Wi-Fi & APIs](../components/wifi.md)
    and [Buttons](../components/buttons.md). Make sure **`button.py`**,
    **`ssd1306.py`**, **`wifi.py`** and **`secrets.py`** (with your Wi-Fi
    name and password) are saved on your ESP32 (see
    [Saving Programs to the Board](../getting-started/saving-programs.md)).

## Wiring

| Part | Pin | Connects to |
|---|---|---|
| DHT11 module | + / VCC | **3V3** |
| | OUT / DATA | GPIO **19** |
| | – / GND | **GND** |
| OLED | GND | **GND** |
| | VCC | **3V3** |
| | SCL | GPIO **22** |
| | SDA | GPIO **21** |
| Button A | one leg | GPIO **14**, other leg to **GND** |

## Set your location

Near the top of the code are two lines for your location:

```python
LATITUDE = 40.71
LONGITUDE = -74.01
```

These are New York's. Search the web for *"latitude longitude"* and the name
of your town, and paste in your own numbers. North and east are positive;
south and west are negative.

## Plan it out

1. **Set up each component.** The OLED on I2C, the DHT11, and Button A. Then
   connect to Wi-Fi.
2. **Break the job into functions.**
    - `read_indoor()` asks the DHT11 for a new measurement.
    - `read_outdoor()` asks Open-Meteo for the current weather.
    - `format_temp()` and `format_humidity()` turn numbers into short text,
      in °C or °F, or `--` if there's no reading.
    - `draw()` lays everything out on the screen.
3. **Call the functions from the main loop**, each on its own schedule.
   Check the button every loop, the DHT11 every 2 seconds, and the internet
   every 10 minutes.

## Code

Save this to your ESP32 as **`main.py`** so it runs every time the board
powers up. Or just click **Run** in Thonny to try it out.

```python title="weather_station.py"
--8<-- "projects/weather_station.py"
```

## How it works

- **Different jobs, different speeds.** The button needs checking all the
  time, the DHT11 can only take a reading every second or two, and there's
  no point asking the internet about the weather more than every few
  minutes. Each job gets its own "last time I did this" variable
  (`last_indoor`, `last_outdoor`), and the loop checks with
  `time.ticks_diff()` whether enough time has passed.
- **Planning for failure.** `None` means "no reading". Both reading
  functions wrap their work in `try`/`except`, so a loose wire or a Wi-Fi
  hiccup just prints a message and shows `--`. The next attempt usually
  works. Even if Wi-Fi doesn't connect at all, the indoor readings still
  appear.
- **The API answer** is a dictionary. The part we want sits under the key
  `"current"`:

    ```python
    current = response.json()["current"]
    outdoor_temp = current["temperature_2m"]
    ```

    `response.close()` frees the memory the response used. Forget it, and
    after a few hours the ESP32 runs out of memory.
- **°C to °F:** multiply by 9, divide by 5, and add 32. The screen redraws
  as soon as you press the button, so you don't have to wait for the next
  reading.

## Result

After *Connecting…*, the screen splits into two columns: **Inside** on the
left and **Outside** on the right, each with the temperature and humidity.

![What the Weather Station shows on the OLED](../assets/img/diagrams/p-weather-station.svg){ width="360" }

Breathe gently on the DHT11 and watch the indoor humidity climb. Press
Button A to switch to Fahrenheit.

## Make it your own

- **Colour-coded:** add an [RGB LED](../components/rgb-led.md) that glows blue
  when it's cold outside and orange when it's warm.
- **More weather:** Open-Meteo can also tell you the wind speed
  (`wind_speed_10m`) or whether it's raining (`precipitation`). Add them
  to the URL's `current=` list and put them on a second screen page.
- **Min and max:** keep track of the lowest and highest indoor temperature
  since the board started.
- **Better sensor:** a DHT22 is more accurate than a DHT11 and reads tenths
  of a degree. Change `dht.DHT11` to `dht.DHT22`.
