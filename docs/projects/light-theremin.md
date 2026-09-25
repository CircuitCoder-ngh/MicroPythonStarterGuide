# Project: Light Theremin

<img src="../../assets/img/icons/light-sensor.svg" alt="" class="cc-icon">

A **theremin** is a spooky-sounding electronic instrument that you play
without touching it: you just wave your hands near it. Yours will work the
same way. Move your hand over a light sensor, and the shadow bends the pitch
of the buzzer up and down.

## Objective

- For the first **5 seconds**, the program **calibrates**: it learns the
  darkest and brightest light levels while you wave your hand over the
  sensor.
- After that, **more light = higher pitch**, and **less light = lower pitch**.
- **Button A** mutes and unmutes the sound.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × photoresistor (light sensor)
- [x] 1 × 10 kΩ resistor
- [x] 1 × passive piezo buzzer
- [x] 1 × push button
- [x] Jumper wires
</div>

!!! note "Before you start"
    This project uses what you learned in [Light Sensors](../components/light-sensors.md),
    [Piezo Buzzers](../components/buzzers.md) and [Buttons](../components/buttons.md).
    Make sure **`button.py`** is saved on your ESP32 (see
    [Saving Programs to the Board](../getting-started/saving-programs.md)).

## Wiring

| Part | Pin | Connects to |
|---|---|---|
| Photoresistor | one leg | **3V3** |
| | other leg | GPIO **36** (VP) |
| 10 kΩ resistor | one end | GPIO **36** (same row as the photoresistor) |
| | other end | **GND** |
| Buzzer | + leg | GPIO **26** |
| | – leg | **GND** |
| Button A | one leg | GPIO **14**, other leg to **GND** |

!!! tip
    Point the light sensor up towards a ceiling light or a window. The more
    light there is in the room, the bigger the difference your hand makes.

## Plan it out

1. **Set up each component.** The light sensor is an ADC input, the buzzer
   is a PWM output, and the button uses the `Button` class.
2. **Break the job into functions.**
    - `calibrate()` watches the sensor for 5 seconds and remembers the
      lowest and highest readings it sees.
    - `light_to_pitch()` turns a light reading into a frequency, using the
      calibrated range.
    - `toggle_mute()` flips the sound on and off.
3. **Call the functions from the main loop.** Calibrate once, then keep
   reading the light and updating the pitch, while also checking the
   button.

## Code

Save this to your ESP32 as **`main.py`** so it runs every time the board
powers up. Or just click **Run** in Thonny to try it out.

```python title="light_theremin.py"
--8<-- "projects/light_theremin.py"
```

## How it works

- **Why calibrate?** Every room is different. At midday by a window your
  sensor might read 50000; at night under a lamp, maybe 15000. Instead of
  guessing, the program *measures* the real range for your room when it
  starts. The board's built-in LED stays on while it calibrates, so you
  know when to wave.
- `min()` and `max()` keep track of the lowest and highest readings so far.
  If you forget to wave (so the readings barely change), the program falls
  back to the full 0–65535 range so it still makes a sound.
- `light_to_pitch()` first **clamps** the reading into the calibrated range
  (a cloud might make the room darker than it was during calibration), then
  uses the same "map one range onto another" line you've seen in the
  [Music Machine](music-machine.md):

    ```python
    LOWEST_NOTE + (reading - darkest) * (HIGHEST_NOTE - LOWEST_NOTE) // span
    ```

## Result

When the program starts, the blue LED on the board lights up. Wave your
hand up and down over the sensor until it goes out. Now the buzzer sings.
Hover your hand close to the sensor for a low note, and pull it away for a
high one. Press Button A to give everyone's ears a rest.

## Make it your own

- **Flip it:** make *less* light give a *higher* note by swapping
  `LOWEST_NOTE` and `HIGHEST_NOTE`.
- **Real notes:** snap the pitch to the nearest note of a scale so it sounds
  more musical. (The [Music Machine](music-machine.md) challenge shows how.)
- **Volume control:** add a potentiometer on GPIO 34 and use it to set the
  duty cycle from 0 to 32768.
- **Two-handed:** add a second light sensor on GPIO 39 (VN). Use one hand
  for pitch and the other for volume, like a real theremin.
