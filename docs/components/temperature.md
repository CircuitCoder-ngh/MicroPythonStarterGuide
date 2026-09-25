# Temperature & Humidity

<img src="../../assets/img/icons/temperature.svg" alt="" class="cc-icon">

The **DHT11** is a small blue sensor that measures both **temperature** and
**humidity** (how much water vapour is in the air). It's a new kind of
input: instead of a voltage, it sends its readings back as a short burst of
**digital data** down a single wire. MicroPython already knows how to decode
it, so reading it takes just two lines.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × DHT11 module (3 pins, on a small board), or a DHT22
- [x] 3 × jumper wires
- [x] The RGB LED from the [RGB LEDs](rgb-led.md) lesson (for the challenge)
</div>

## Hardware

The DHT11 module has three pins, usually labelled on the board:

| DHT11 pin | Connect to |
|---|---|
| **+** or **VCC** | ESP32 **3V3** |
| **OUT** or **S** (data) | ESP32 **GPIO 19** |
| **–** or **GND** | ESP32 **GND** |

!!! note "Bare 4-pin sensors"
    If your DHT11 is just the blue sensor with **four** legs (no small
    board), it needs a 10 kΩ **pull-up resistor** between the data leg
    (leg 2) and 3V3. Leg 1 is VCC, leg 4 is GND, and leg 3 isn't used.
    The modules have this resistor built in.

!!! info "DHT11 vs DHT22"
    The **DHT22** (usually white) is the DHT11's more accurate big brother.
    It measures to a tenth of a degree and works below freezing. It wires up
    the same way; just change `dht.DHT11` to `dht.DHT22` in the code.

## Software

```python title="dht_read.py"
--8<-- "lessons/dht_read.py"
```

- `import dht` loads the DHT driver that comes built into MicroPython.
- `sensor.measure()` asks the sensor to take a reading. Then
  `sensor.temperature()` (in °C) and `sensor.humidity()` (in %) return
  the results.
- `temp_c * 9 / 5 + 32` converts Celsius to Fahrenheit. In the f-string,
  `{temp_f:.1f}` means "show one digit after the decimal point".
- Breathe gently on the sensor: the humidity should jump up within a few
  seconds.

### Handling a failed reading

Every now and then, the sensor's data gets garbled on the way to the ESP32
and `measure()` raises an `OSError`. Without a plan, that would crash your
program. The `try:` / `except OSError:` block catches the error, prints a
message, and lets the loop carry on to the next reading.

This pattern is worth remembering. Anything that talks to the outside world,
from sensors to Wi-Fi, can occasionally fail, and good programs expect it.

!!! warning "Don't read too often"
    The DHT11 can only take **one reading per second**, and the DHT22 one
    every **two seconds**. Ask more often and you'll get errors or the same
    old reading again.

## Challenge

Turn the RGB LED into a comfort indicator: **blue** when the room is too
cold, **green** when it's comfortable, and **red** when it's too hot.

??? example "Show a solution"

    ```python title="dht_comfort.py"
    --8<-- "lessons/dht_comfort.py"
    ```

    Hold the sensor between your fingers to warm it up and watch the colour
    change. Adjust `TOO_COLD` and `TOO_HOT` to suit your room.

**Next up:** [Touch Sensors](touch.md): buttons made out of thin air (and a
wire).
