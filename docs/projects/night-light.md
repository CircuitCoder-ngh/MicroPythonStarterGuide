# Project: Night Light

<img src="../../assets/img/icons/neopixel.svg" alt="" class="cc-icon">

Build a lamp that looks after itself. When the room gets dark, a ring of
NeoPixels fades up to a cosy warm glow, and when the lights come back on,
it fades away again. Touch a coin on the side to switch to a rainbow or a
slow colour fade.

## Objective

- In **auto** mode, the ring glows warm white **only when it's dark**.
- **Touching the pad** (a coin or foil on GPIO 4) steps through the modes:
  **auto warm white → rainbow → colour fade → off**, then back round.
- The light **fades** smoothly between on and off, instead of snapping.
- It mustn't **flicker** when the room is right on the edge of dark.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × NeoPixel ring or stick (8 LEDs)
- [x] 1 × photoresistor (light sensor)
- [x] 1 × 10 kΩ resistor
- [x] 1 × coin, or a square of aluminium foil, for the touch pad
- [x] Jumper wires
</div>

!!! note "Before you start"
    This project uses what you learned in [NeoPixels](../components/neopixels.md),
    [Light Sensors](../components/light-sensors.md) and
    [Touch Sensors](../components/touch.md). It doesn't need any library
    files: `neopixel` comes built into MicroPython.

## Wiring

| Part | Pin | Connects to |
|---|---|---|
| NeoPixel ring | DIN (data in) | GPIO **23** |
| | 5V / VCC | **VIN** |
| | GND | **GND** |
| Photoresistor | one leg | **3V3** |
| | other leg | GPIO **36** (VP) |
| 10 kΩ resistor | one end | GPIO **36** (same row as the photoresistor) |
| | other end | **GND** |
| Touch pad | jumper wire | GPIO **4**. Tape a coin or foil to the other end. |

!!! tip
    Keep the light sensor **pointing away** from the NeoPixels. Otherwise the
    lamp turns on, sees its own light, decides it's daytime, and turns off
    again!

## Plan it out

1. **Set up each component.** The light sensor is an ADC input, the ring is
   a `NeoPixel` object, and the touch pad is a `TouchPad`.
2. **Break the job into functions.**
    - `calibrate_touch()` measures the pad when nobody's touching it.
    - `check_touch()` moves to the next mode once per touch.
    - `check_darkness()` decides whether it's dark, using two thresholds.
    - `wheel()` turns a number into a rainbow colour, and `scaled()` dims a
      colour.
    - `draw()` paints the ring for the current mode.
3. **Call the functions from the main loop.** Every 20 ms: check the touch
   pad, check the light, work out how bright the lamp *should* be, fade a
   little towards that, and redraw.

## Code

Save this to your ESP32 as **`main.py`** so it runs every time the board
powers up. Or just click **Run** in Thonny to try it out.

```python title="night_light.py"
--8<-- "projects/night_light.py"
```

## How it works

- **Hysteresis** is the trick that stops the flickering. If there were only
  one threshold, a room right on the edge would bounce above and below it,
  and the lamp would flash on and off. Instead, it takes a *darker* reading
  (`DARK`) to switch on than it does to switch off (`BRIGHT`). In between,
  `is_dark` simply keeps its last value.
- **Fading:** the loop doesn't jump straight to the brightness it wants.
  Every 20 ms it moves `level` just 0.02 closer to the `target`, so a full
  fade takes about a second.
- **Touch:** on the ESP32 a touch pad's reading **drops** when you touch it.
  `calibrate_touch()` measures the normal reading at start-up, and anything
  below 70 % of that counts as a touch. `was_touched` makes sure one long
  touch only changes the mode once.
- `wheel()` walks around the colour wheel: red → green → blue → back to red.
  In **rainbow** mode each LED gets a different position on the wheel, and
  `step` slowly spins them round. In **colour fade** mode the whole ring
  shares one colour that slowly changes.

!!! tip "Tuning the thresholds"
    Add `print(light.read_u16())` to the loop and watch the numbers in the
    Shell with the room lights on and off. Pick `DARK` a bit above your "lights
    off" number and `BRIGHT` a bit below your "lights on" number.

## Result

Cover the light sensor with your hand (or turn off the lights) and the ring
fades up to a soft orange-white. Uncover it and the glow fades away. Touch
the coin, and the ring bursts into a spinning rainbow. Touch it again for a
slow, calm colour fade, and once more to switch it off.

## Make it your own

- **Cheaper version:** use an [RGB LED](../components/rgb-led.md) instead of
  a NeoPixel ring. You'll only have one colour at a time, but the colour
  fade looks great through a ping-pong ball diffuser.
- **Sleep timer:** after 30 minutes on, fade out slowly. Handy for falling
  asleep.
- **Brightness knob:** add a potentiometer on GPIO 34 to set `BRIGHTNESS`.
- **Lampshade:** a paper cup, a frosted jar or a 3D-printed shade turns
  a breadboard into something you'd actually keep on a shelf.
