# Line Sensors

<img src="../../assets/img/icons/line-sensor.svg" alt="" class="cc-icon">

A **line sensor** tells the robot whether it's over a dark line or a light
floor. Two of them, side by side under the front of the robot, are all it
takes to follow a track of black tape. You'll try them out on the desk first,
before they go on the robot.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 2 × TCRT5000 line-tracking modules
- [x] Female-to-male jumper wires
- [x] A piece of white paper and some black electrical tape (or a thick
      black marker)
</div>

## How it works

Look at the underside of a TCRT5000 module. There are two little "eyes"
side by side:

- An **infrared LED**, which shines invisible infrared light downwards.
- A **phototransistor**, which measures how much of that light bounces back.

**White and light surfaces reflect** lots of infrared light. **Black
surfaces absorb** it. A small comparator chip on the module compares the
reflected light to a threshold and sets the **DO** (digital output) pin to
either 1 or 0. It's a digital input, just like a button.

!!! tip "See the invisible"
    Point your phone's camera at the sensor's LED. Many phone cameras can see
    infrared, so you'll see it glowing faintly purple.

The module also has a small **indicator LED** on top that lights up when the
sensor sees a reflection, and a **blue potentiometer** that sets the
threshold (the sensitivity).

## Hardware

| Module pin | Connects to |
|---|---|
| **VCC** | ESP32 **3V3** |
| **GND** | ESP32 **GND** |
| **DO** (left sensor) | ESP32 **GPIO 34** |
| **DO** (right sensor) | ESP32 **GPIO 35** |
| **AO** (if there is one) | Not used |

Power the modules from **3V3**, not VIN, so that their output never goes
above 3.3 V.

!!! note "Input-only pins"
    GPIO 34 and 35 are input-only pins with no internal pull-up resistors. That's
    fine here, because the module drives the DO pin itself.

## Software

```python title="line_sensor_read.py"
--8<-- "robot/line_sensor_read.py"
```

Run it and hold each sensor about **5–10 mm** above the white paper, then
over the black tape. The printout should change between `floor` and `LINE`.

### Which way round?

On most TCRT5000 modules:

| Surface | Reflection | Indicator LED | DO |
|---|---|---|---|
| White floor | Lots | On | **0** |
| Black line | Hardly any | Off | **1** |

That's why the code has `LINE_IS = 1`. If your modules work the other way
round (the printout says `LINE` over the white paper), change it to
`LINE_IS = 0`. Every robot program uses this same setting.

### Adjusting the sensitivity

If the sensor always says the same thing, adjust its potentiometer with a
small screwdriver:

1. Hold the sensor over the **white** paper at the height it will be on the
   robot.
2. Turn the potentiometer until the indicator LED **just** switches on.
3. Move it over the black tape. The LED should go **off**. If it doesn't,
   turn the potentiometer back a little and try again.

!!! warning "Sunlight confuses them"
    Sunlight contains lots of infrared, which can swamp the sensor. Line
    following works best indoors, away from bright windows.

## Challenge

Make the ESP32's built-in LED (GPIO 2) light up only when **both** sensors
are over the line at once, like when the robot crosses a finish line made of
a strip of tape across the track.

??? example "Show a solution"

    ```python
    import time
    from machine import Pin

    LINE_IS = 1
    left_sensor = Pin(34, Pin.IN)
    right_sensor = Pin(35, Pin.IN)
    led = Pin(2, Pin.OUT)

    while True:
        both = left_sensor.value() == LINE_IS and right_sensor.value() == LINE_IS
        led.value(both)
        time.sleep_ms(20)
    ```

**Next up:** time to put it all together. [Build the Robot](build.md).
