# Project: Parking Sensor

<img src="../../assets/img/icons/ultrasonic.svg" alt="" class="cc-icon">

Modern cars beep faster and faster as you reverse towards a wall. Now you
can build that sensor yourself. An ultrasonic sensor measures the distance,
an RGB LED shows green, yellow or red, and the buzzer beeps quicker the
closer you get, until it becomes one long "STOP!" tone.

## Objective

| Distance | LED | Buzzer |
|---|---|---|
| Further than **50 cm** (or nothing in range) | 🟢 Green | Silent |
| **25–50 cm** | 🟡 Yellow | Slow beeps |
| **10–25 cm** | 🔴 Red | Beeps getting faster |
| Closer than **10 cm** | 🔴 Red | One continuous tone |

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × HC-SR04P ultrasonic sensor (or HC-SR04 with a voltage divider)
- [x] 1 × RGB LED (common cathode)
- [x] 3 × 220 Ω resistors
- [x] 1 × passive piezo buzzer
- [x] Jumper wires
</div>

!!! note "Before you start"
    This project uses what you learned in [Ultrasonic Sensors](../components/ultrasonic.md),
    [RGB LEDs](../components/rgb-led.md) and [Piezo Buzzers](../components/buzzers.md).
    Make sure **`distance.py`** is saved on your ESP32 (see
    [Saving Programs to the Board](../getting-started/saving-programs.md)).

## Wiring

| Part | Pin | Connects to |
|---|---|---|
| Ultrasonic sensor | VCC | **3V3** (HC-SR04P) or **VIN** (5 V HC-SR04) |
| | TRIG | GPIO **5** |
| | ECHO | GPIO **39** (VN). Through a voltage divider for a 5 V sensor |
| | GND | **GND** |
| RGB LED | red leg | 220 Ω resistor → GPIO **16** |
| | green leg | 220 Ω resistor → GPIO **17** |
| | blue leg | 220 Ω resistor → GPIO **18** |
| | common (longest) leg | **GND** |
| Buzzer | + leg | GPIO **26** |
| | – leg | **GND** |

## Plan it out

1. **Set up each component.** Create a `DistanceSensor` for the ultrasonic
   sensor, a PWM output for the buzzer, and a PWM output for each colour of
   the RGB LED.
2. **Break the job into functions.**
    - `set_colour(r, g, b)` sets the LED to any colour (0–255 for each).
    - `smoothed_distance()` measures, and returns the middle of the last
      three readings.
    - `beep_gap_ms(cm)` works out how long to wait between beeps.
    - `update(cm)` picks the colour and decides whether the buzzer should be
      sounding *right now*.
3. **Call the functions from the main loop.** Measure, update, repeat.

## Code

Save this to your ESP32 as **`main.py`** so it runs every time the board
powers up. Or just click **Run** in Thonny to try it out.

```python title="parking_sensor.py"
--8<-- "projects/parking_sensor.py"
```

## How it works

- **Smoothing with a median.** Ultrasonic sensors sometimes return a wild
  reading, for example when the sound bounces off something at an angle.
  `smoothed_distance()` keeps the last three good readings and returns the
  **middle** one after sorting. One odd value gets outvoted by the other
  two, and the LED doesn't flash the wrong colour. If the sensor hears no
  echo at all (`None`), that reading is simply skipped.
- **Beeping without `sleep()`.** If the loop used `time.sleep()` between
  beeps, it couldn't measure the distance while it waited. Instead,
  `last_beep` remembers when the last beep started. Each time round the
  loop, the program checks how long ago that was:
    - less than `BEEP_LENGTH_MS` ago: the buzzer is **on**;
    - after that: the buzzer is **off**;
    - once the whole gap has passed, a new beep starts.

    Because this check runs every loop, the beeping speeds up the moment
    something moves closer.
- `beep_gap_ms()` maps the distance onto the gap between beeps: 600 ms at
  25 cm, down to just 80 ms at 10 cm.
- `set_colour()` multiplies by 257 to turn the familiar 0–255 colour scale
  into the 0–65535 range that `duty_u16()` expects (255 × 257 = 65535).

## Result

Point the sensor at the ceiling and the LED glows green. Slowly lower your
hand towards it. At about 50 cm the LED turns yellow and slow beeps start.
The beeps get faster as you get closer and the LED turns red, until below
10 cm the buzzer holds one long tone. The Shell prints each distance too.

## Make it your own

- **Park your bike (or car):** stick the sensor to a garage wall at bumper
  height, and set `STOP_CM` to where you want to stop.
- **Silent mode:** add Button A to mute the buzzer and use only the colours.
- **More colour:** fade smoothly from green to red instead of jumping
  between three colours.
- **Distance display:** add the [OLED](../components/oled.md) and show the
  distance in big numbers.
