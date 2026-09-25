# Touch Sensors

<img src="../../assets/img/icons/touch.svg" alt="" class="cc-icon">

This lesson needs **no new parts at all**. The ESP32 has **capacitive touch
sensing** built in, the same idea as a phone touchscreen. Ten of its pins
can tell when you touch them (or anything conductive wired to them), so a
jumper wire, a coin, a sheet of foil or even a banana can become a button.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 2 × jumper wires
- [x] Optional: coins, aluminium foil, or pieces of fruit
- [x] The LED from the [LEDs](leds.md) lesson
</div>

## Hardware

Your body can hold a tiny electrical charge (that's its **capacitance**).
The ESP32 constantly charges and discharges each touch pin and times how
long that takes. When your finger touches the pin, it adds your body's
capacitance, and the timing changes.

### Wiring

| From | To |
|---|---|
| ESP32 **GPIO 4** | A jumper wire with its other end free (pad A) |
| ESP32 **GPIO 15** | A jumper wire with its other end free (pad B) |

That's it! Touch the metal end of each wire to use it. To make a bigger pad,
press the loose end of the wire onto a coin or a square of foil and hold it
down with tape.

!!! note "Which pins can sense touch?"
    On the classic ESP32, touch works on GPIO **0, 2, 4, 12, 13, 14, 15,
    27, 32 and 33**. This guide uses 4 and 15, which aren't needed by
    anything else in the [pin plan](../reference/esp32-pins.md).

## Software

### Reading the raw value

```python title="touch_read.py"
--8<-- "lessons/touch_read.py"
```

Run it and watch the numbers, then touch the end of the wire. On the ESP32,
the number gets **smaller** when you touch the pin. You might see something
like 600 untouched and 150 touched.

!!! tip "Try it in the REPL"
    ```pycon
    >>> from machine import Pin, TouchPad
    >>> pad = TouchPad(Pin(15))
    >>> pad.read()
    587
    ```

### Turning it into a button

The exact numbers depend on your board, the length of the wire, and even the
humidity in the room, so picking one fixed threshold for "touched" doesn't
work everywhere. Instead, this code **measures a baseline** when it starts
and treats any reading below 70 % of it as a touch:

```python title="touch_button.py"
--8<-- "lessons/touch_button.py"
```

- `TouchButton` is a **class**, a bit like the `Button` class from the
  [Buttons](buttons.md) lesson. Each touch pad gets its own object with its
  own threshold.
- `__init__` runs once, when the object is created. It averages 10 readings
  to find the untouched **baseline**, so **don't touch the wires while the
  program starts**.
- `was_touched()` only returns `True` at the moment a finger lands, just
  like `Button.was_pressed()`. `_was_down` remembers what happened last
  time.
- If a pad is too twitchy, lower the `sensitivity` (for example `0.6`). If
  it doesn't respond, raise it (for example `0.8`).

!!! tip "Longer wires, weaker touches"
    Very long wires and large pads pick up more "noise". Keep the wires
    short, and if a pad misbehaves, restart the program to take a fresh
    baseline.

## Challenge

Make pad A turn the LED on and pad B turn it off, like a pair of light
switches. Then try swapping the wires for two pieces of fruit!

??? example "Show a hint"

    Replace the two `if` blocks in the main loop:

    ```python
    if pad_a.was_touched():
        led.on()
    if pad_b.was_touched():
        led.off()
    ```

**Next up:** [NeoPixels](neopixels.md): strings of colour LEDs you control
one by one.
