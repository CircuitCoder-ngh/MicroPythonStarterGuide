# Project: Touch Piano

<img src="../../assets/img/icons/touch.svg" alt="" class="cc-icon">

The ESP32 can feel your touch on ten of its pins, with no buttons needed.
In this project you'll wire seven of them to anything that conducts
electricity (squares of foil, coins, even bananas) and turn them into the
keys of a piano.

## Objective

- Seven touch keys play the notes **C D E F G A B**.
- A note plays for **as long as you hold** its key, and stops when you let
  go.
- If you touch several keys at once, the **lowest** note wins.
- *Optional:* a NeoPixel stick lights up in a different colour for each note.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × passive piezo buzzer
- [x] 7 × jumper wires (male-to-male, or with crocodile clips)
- [x] 7 × things to touch: foil squares, coins, pieces of fruit…
- [x] Tape
- [x] *Optional:* 1 × NeoPixel stick (8 LEDs)
</div>

!!! warning "This project borrows pins from the plan"
    The ESP32 only has ten touch-capable pins, and many are already used in
    the [pin plan](../reference/esp32-pins.md). **Unplug the servo (13),
    Button A (14), the LED (27), the motion sensor (33) and Button C (32)**
    before you start.

!!! note "Before you start"
    This project uses what you learned in [Touch Sensors](../components/touch.md)
    and [Piezo Buzzers](../components/buzzers.md). It doesn't need any
    library files.

## Wiring

| Key | Note | Connects to |
|---|---|---|
| 1 | C | GPIO **4** |
| 2 | D | GPIO **15** |
| 3 | E | GPIO **13** |
| 4 | F | GPIO **14** |
| 5 | G | GPIO **27** |
| 6 | A | GPIO **33** |
| 7 | B | GPIO **32** |
| Buzzer | + leg | GPIO **26** |
| | – leg | **GND** |
| *Optional:* NeoPixel stick | DIN / 5V / GND | GPIO **23** / **VIN** / **GND** |

Tape one end of each key's jumper wire to its foil square (or push it into
the fruit), and lay the keys out in a row on the table, lowest note on the
left.

!!! tip "Making good keys"
    Make each key about the size of a fingertip or bigger. Keep the wires
    apart from each other, and don't let the keys touch. Your body is part
    of the circuit, so you don't need a ground wire: just touch the key.

## Plan it out

1. **Set up each component.** Make a list called `KEYS` holding each note's
   name, pin and frequency. Create a `TouchPad` for every key and a PWM
   output for the buzzer.
2. **Break the job into functions.**
    - `calibrate()` measures every key while nobody is touching it (its
      *baseline*).
    - `pressed_key()` checks the keys from lowest to highest and returns the
      first one that's being touched.
    - `show_colour()` lights the NeoPixels, if you have them.
3. **Call the functions from the main loop.** Find out which key is
   touched. If it's different from last time, start the new note (or stop
   the sound).

## Code

Save this to your ESP32 as **`main.py`** so it runs every time the board
powers up. Or just click **Run** in Thonny to try it out.

```python title="touch_piano.py"
--8<-- "projects/touch_piano.py"
```

## How it works

- **Every key is different.** A long wire, a big foil square and a banana all
  give different readings, so one threshold for all of them wouldn't work.
  `calibrate()` averages 20 readings per key to find each one's own
  **baseline**. A key counts as touched when its reading drops below 70 % of
  its baseline (`SENSITIVITY`).
- **Keep your hands off at the start!** If you're touching a key while it
  calibrates, that key's baseline will be too low and it'll never trigger.
  Press the board's **EN/RST** button to calibrate again.
- `pads = [TouchPad(Pin(pin)) for name, pin, freq in KEYS]` is a **list
  comprehension**: a compact way of building a list with a loop. It makes
  one `TouchPad` for every entry in `KEYS`.
- `current` remembers which key was playing last time. The buzzer is only
  changed when the key **changes**, which keeps the sound clean instead of
  restarting it 100 times a second.
- To turn on the optional NeoPixels, change `USE_PIXELS = False` to `True`.
  The `neopixel` module is only imported if you use it.

## Result

Touch the first key and the buzzer plays a C. Slide your finger along the
keys and it plays up the scale. Try *Twinkle Twinkle Little Star*: C C G G
A A G, F F E E D D C.

## Make it your own

- **Fruit keyboard:** swap the foil for bananas, apples or oranges. It works,
  and it's much funnier.
- **Tune your sensitivity:** if keys trigger when your hand is nearby, lower
  `SENSITIVITY` to 0.6. If they're hard to trigger, raise it to 0.8.
- **Octave switch:** make the lowest key a "shift" key that doubles every
  other note's frequency while it's held (an octave higher).
- **Record and play back:** store `(note, milliseconds)` pairs in a list as
  you play, then replay your tune when you touch two keys at once.
