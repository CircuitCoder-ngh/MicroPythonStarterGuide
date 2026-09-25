# NeoPixels

<img src="../../assets/img/icons/neopixel.svg" alt="" class="cc-icon">

**NeoPixels** (their technical name is **WS2812B**) are RGB LEDs with a tiny
chip built into each one. You can chain dozens or even hundreds of them
together, and set every single pixel to its own colour, all from **one
GPIO pin**. They're what's inside most LED strips, light-up keyboards and
colour-changing lamps.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × WS2812B NeoPixel ring or stick with 8 LEDs (12 or 16 work too)
- [x] 3 × jumper wires (you may need to solder header pins onto the ring)
</div>

## Hardware

Each pixel receives a stream of colour data, keeps the first colour for
itself, and passes the rest along to the next pixel in the chain. That's why
one data wire is enough.

| NeoPixel pin | Connect to |
|---|---|
| **5V** / **VCC** / **PWR** | ESP32 **VIN** (5 V) |
| **DIN** / **IN** (data in) | ESP32 **GPIO 23** |
| **GND** | ESP32 **GND** |

Rings and sticks often have a **DOUT** (data out) pin too. It's for chaining
another strip on the end, so leave it unconnected.

!!! warning "Mind the power"
    Each pixel can draw about **60 mA** at full white, full brightness. Eight
    pixels at full blast is nearly half an amp, about as much as a computer
    USB port gives. The examples here keep brightness **low**, which looks
    plenty bright indoors. For more than about 16 pixels at high brightness,
    power them from a separate 5 V supply (and connect its GND to the
    ESP32's GND).

!!! note "3.3 V data"
    NeoPixels are powered by 5 V but get their data from the ESP32's 3.3 V
    pin. With short wires this almost always works fine. If your pixels
    flicker or show random colours, shorten the data wire.

## Software

MicroPython has a NeoPixel driver built in:

```python title="neopixel_basics.py"
--8<-- "lessons/neopixel_basics.py"
```

- `NeoPixel(Pin(23), 8)` creates a driver for 8 pixels on GPIO 23.
- `pixels` works a lot like a **list**: `pixels[0]` is the first pixel,
  and you set it to a colour tuple `(red, green, blue)`, each 0–255.
- Nothing lights up until you call `pixels.write()`, which sends every
  colour down the wire at once. That way all the pixels change together.

!!! tip "Try it in the REPL"
    ```pycon
    >>> from machine import Pin
    >>> from neopixel import NeoPixel
    >>> pixels = NeoPixel(Pin(23), 8)
    >>> pixels.fill((0, 20, 0))
    >>> pixels.write()
    ```
    `fill()` sets **every** pixel to the same colour.

### A chasing light

```python title="neopixel_chase.py"
--8<-- "lessons/neopixel_chase.py"
```

- Each time round the loop, `fill((0, 0, 0))` clears all the pixels, one
  pixel is lit, and `position` moves on by one.
- `(position + 1) % NUM_PIXELS` uses the **remainder** operator to wrap
  from the last pixel back to 0, so the dot runs round and round.

### Rainbow

```python title="neopixel_rainbow.py"
--8<-- "lessons/neopixel_rainbow.py"
```

- `wheel()` turns any number into a colour on the **colour wheel**: 0 is
  red, about 85 is green, about 170 is blue, and 255 is back to red. It's
  the same cross-fade as the last example in [RGB LEDs](rgb-led.md), packed
  into a function.
- Each pixel gets a colour spread evenly around the wheel, and adding
  `offset` each frame makes the whole rainbow spin.
- `BRIGHTNESS` scales every colour down. Try `1.0` for a moment (it's
  **bright**), then put it back.

## Challenge

Make a **level meter**: turn the potentiometer on GPIO 34 and light up more
pixels the further you turn it: green for the first few, then yellow, then
red at the top.

??? example "Show a hint"

    Scale the potentiometer reading to the number of pixels:
    `lit = pot.read_u16() * NUM_PIXELS // 65535`. Then loop over every
    pixel: if its number is less than `lit`, give it a colour based on its
    position; otherwise set it to `(0, 0, 0)`. Don't forget
    `pixels.write()` at the end!

**Next up:** [Ultrasonic Sensors](ultrasonic.md): measure distance with
sound, like a bat.
