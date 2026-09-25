# Project: Sonar Radar

<img src="../../assets/img/icons/ultrasonic.svg" alt="" class="cc-icon">

This is real mechatronics: **sensing**, **motion** and a **display**
working together. A servo swings an ultrasonic sensor from side to side like
a lighthouse, and the OLED draws a radar screen with a sweeping line and a
dot wherever it finds something.

## Objective

- The servo sweeps the sensor from **0° to 180°** and back, forever.
- At each step, the sensor measures the distance straight ahead.
- The OLED shows a **radar display**: range rings, the sweep line, and a
  **dot** for every object within **100 cm**.
- Old dots disappear when the sweep passes over them and they're no longer
  there.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × SG90 servo motor
- [x] 1 × HC-SR04P ultrasonic sensor (or HC-SR04 with a voltage divider)
- [x] 1 × SSD1306 OLED screen (128 × 64, I2C)
- [x] 4 × female-to-male jumper wires (so the sensor can move freely)
- [x] Tape, a rubber band or hot glue
</div>

!!! note "Before you start"
    This project uses what you learned in [Servo Motors](../components/servos.md),
    [Ultrasonic Sensors](../components/ultrasonic.md) and
    [OLED Screens](../components/oled.md). Make sure **`distance.py`** and
    **`ssd1306.py`** are saved on your ESP32 (see
    [Saving Programs to the Board](../getting-started/saving-programs.md)).

## Build the scanner

1. Push the long single-arm (or cross) horn onto the servo.
2. Attach the ultrasonic sensor to the horn so its two "eyes" face outwards,
   using tape, a rubber band, or a dab of hot glue on the back of the
   sensor. Make sure nothing covers the eyes.
3. Connect the sensor with **female-to-male jumper wires** so it can turn
   without pulling anything out of the breadboard.
4. Tape the servo down to the table (or a small box) so it doesn't walk
   away while it sweeps.

## Wiring

| Part | Pin | Connects to |
|---|---|---|
| Servo | brown / black | **GND** |
| | red | **VIN** |
| | orange / yellow | GPIO **13** |
| Ultrasonic sensor | VCC | **3V3** (HC-SR04P) or **VIN** (5 V HC-SR04) |
| | TRIG | GPIO **5** |
| | ECHO | GPIO **39** (VN). Through a voltage divider for a 5 V sensor |
| | GND | **GND** |
| OLED | GND | **GND** |
| | VCC | **3V3** |
| | SCL | GPIO **22** |
| | SDA | GPIO **21** |

## Plan it out

1. **Set up each component.** The servo (PWM at 50 Hz), the
   `DistanceSensor`, and the OLED. Make an empty dictionary called `blips`
   to remember what was found at each angle.
2. **Break the job into functions.**
    - `set_angle()` points the servo, as in the servo lesson.
    - `polar_to_screen()` turns "an angle and a distance" into x, y pixels.
    - `draw_grid()` draws the range rings and baseline.
    - `draw()` draws the grid, the sweep line and every blip.
    - `scan(angle)` moves, waits, measures, remembers and redraws.
3. **Call the functions from the main loop.** Two `for` loops: one sweeping
   up from 0° to 180°, the other sweeping back down.

## Code

Save this to your ESP32 as **`main.py`** so it runs every time the board
powers up. Or just click **Run** in Thonny to try it out.

```python title="sonar_radar.py"
--8<-- "projects/sonar_radar.py"
```

## How it works

- **Polar to screen coordinates.** The sensor gives us an *angle* and a
  *distance*, but the screen needs *x* and *y*. That's exactly what
  trigonometry is for:

    ```python
    x = CENTRE_X + length * cos(angle)
    y = CENTRE_Y - length * sin(angle)
    ```

    `math.radians()` converts degrees into radians, the unit that `cos()`
    and `sin()` expect. The `y` line uses **minus** because on the screen
    y grows *downwards*, but we want 90° to point *up*.
- **Scaling distance to pixels.** The radar's radius is 60 pixels and it
  shows up to 100 cm, so each blip is drawn at `cm * 60 // 100` pixels from
  the centre.
- **The `blips` dictionary** uses the angle as the key and the distance as
  the value. Each time the sweep reaches an angle, that angle's entry is
  **replaced** with the new reading, or **deleted** if nothing's there any
  more. That's how old dots vanish as the sweep line passes.
- **Let the servo settle.** After each move, `time.sleep_ms(SETTLE_MS)`
  gives the servo 40 ms to arrive before measuring. Measure too early and
  you'd be pinging while the sensor is still turning.

## Result

The servo starts ticking across in 3° steps and the radar screen comes to
life: a line sweeps around the half circle, and dots appear where your
walls, cups and hands are. Put a mug 30 cm in front and watch a cluster of
dots appear at the matching spot on the screen. The Shell prints every
angle and distance too.

![What the Sonar Radar shows on the OLED](../assets/img/diagrams/p-sonar-radar.svg){ width="360" }

## Make it your own

- **Speed vs. detail:** change `STEP` to 1 for a sharper picture, or 6 for
  a faster sweep.
- **Intruder alarm:** sound the buzzer if anything appears closer than
  30 cm.
- **Zoom:** add a potentiometer on GPIO 34 that changes `RANGE_CM` between
  30 and 200 cm.
- **Put it on wheels:** this scanning head is exactly what the
  [robot](../robot/index.md) uses to look around before it turns.
