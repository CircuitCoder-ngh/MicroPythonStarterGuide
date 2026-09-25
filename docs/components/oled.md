# OLED Screens

<img src="../../assets/img/icons/oled.png" alt="" class="cc-icon">

A small OLED screen lets your projects show text, numbers and graphics
without needing a computer. The 0.96-inch **SSD1306** display used here has
128 × 64 pixels, each of which you can switch on or off, and it talks to the
ESP32 using **I2C**.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × SSD1306 128×64 I2C OLED display (4 pins: GND, VCC, SCL, SDA)
- [x] 4 × jumper wires
- [x] A potentiometer (for the challenge)
</div>

## Hardware

### What is I2C?

**I2C** (say "eye-squared-see") is a way for chips to exchange data using
just two wires:

- **SDA** (serial data) carries the data.
- **SCL** (serial clock) carries a clock signal that keeps both sides in
  step.

Lots of devices can share the same two wires. Each has its own **address**,
like a house number, so the ESP32 can talk to one at a time. Most SSD1306
screens use address `0x3C`.

### Wiring

| OLED pin | Connect to |
|---|---|
| **GND** | ESP32 **GND** |
| **VCC** | ESP32 **3V3** |
| **SCL** | ESP32 **GPIO 22** |
| **SDA** | ESP32 **GPIO 21** |

The order of the pins differs between screens, so read the labels on yours
rather than going by position.

!!! note "Correction from the first edition"
    The first edition of this guide had SDA and SCL the wrong way round in
    the text. The ESP32's usual I2C pins are **SDA = 21** and **SCL = 22**.

### Check the connection

Run this in Thonny's Shell:

```pycon
>>> from machine import I2C, Pin
>>> i2c = I2C(0, scl=Pin(22), sda=Pin(21))
>>> i2c.scan()
[60]
```

`i2c.scan()` lists the address of every device it finds. `60` is `0x3C`
written as a normal number. If you get `[]`, the ESP32 can't see the
screen: check the wiring, especially that SDA and SCL aren't swapped.

## Install the display driver

The ESP32 doesn't know how to drive an SSD1306 on its own, so you need a
small **driver** module called `ssd1306.py`. Pick one way to install it:

=== "Thonny package manager"

    1. With the ESP32 connected, open **Tools → Manage packages…**
    2. Search for `ssd1306` and install the **micropython-lib** version
       onto the board.

=== "Copy the file"

    1. Download [`ssd1306.py`](https://github.com/CircuitCoder-ngh/MicroPythonStarterGuide/blob/main/code/lib/ssd1306.py)
       (the official driver from micropython-lib).
    2. Save it onto your ESP32 as `ssd1306.py`. See
       [Saving Programs to the Board](../getting-started/saving-programs.md).

=== "Command line"

    ```bash
    mpremote mip install ssd1306
    ```

    See [Command-Line Tools](../reference/command-line.md).

## Software

### Drawing on the screen

```python title="oled_hello.py"
--8<-- "lessons/oled_hello.py"
```

The screen is a grid of pixels. **(0, 0) is the top-left corner**. `x` goes
up to 127 moving right, and `y` goes up to 63 moving **down**.

| Command | What it does |
|---|---|
| `display.fill(c)` | Set every pixel to colour `c` (`0` = off, `1` = on) |
| `display.pixel(x, y, c)` | Set a single pixel |
| `display.text("Hi", x, y, c)` | Write text with its top-left corner at (x, y) |
| `display.line(x1, y1, x2, y2, c)` | Draw a line between two points |
| `display.rect(x, y, w, h, c)` | Draw an outline rectangle, `w` wide and `h` tall |
| `display.fill_rect(x, y, w, h, c)` | Draw a solid rectangle |
| `display.show()` | Send everything you've drawn to the screen |

Each character of text is 8 × 8 pixels, so a line fits **16 characters** and
the screen fits **8 lines**.

!!! tip "Nothing happens?"
    Drawing commands only change a copy of the screen in the ESP32's memory.
    Nothing appears until you call `display.show()`. Forgetting it is the
    most common OLED bug!

### Animation

To animate something, clear the screen, draw the next frame, show it, and
repeat:

```python title="oled_bouncing_ball.py"
--8<-- "lessons/oled_bouncing_ball.py"
```

- `dx` and `dy` are the ball's speed: how many pixels it moves each frame.
- When the ball reaches an edge, flipping the sign of `dx` or `dy` sends it
  back the other way.

## Challenge

Wire a potentiometer to GPIO 34 (see [Potentiometers](potentiometers.md)),
and draw a bar graph that grows and shrinks as you turn the knob, with the
percentage written above it.

??? example "Show a solution"

    ```python title="oled_pot_bar.py"
    --8<-- "lessons/oled_pot_bar.py"
    ```

    Use two knobs to move a drawing point instead, and you've got the
    [Etch-a-Sketch](../projects/etch-a-sketch.md) project!

**Next up:** [Motion Sensors](motion-sensors.md).
