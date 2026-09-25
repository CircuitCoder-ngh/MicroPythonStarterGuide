# Your First Program

Time to make the board do something. There are two ways to run code on it,
and you'll use both all the time:

- **The Shell (REPL)**: type a line, and it runs immediately. Great for
  quick experiments.
- **The editor**: write a whole program, then click **Run**.

## Talk to the board in the Shell

Click next to the `>>>` in Thonny's Shell and type each line, pressing
++enter++ after each one:

```pycon
>>> print("Hello from my ESP32!")
Hello from my ESP32!
>>> 7 * 6
42
```

Everything you just typed ran **on the ESP32**, not on your computer. The
board worked out the answer and sent it back over USB.

Now turn on the board's built-in LED. Most ESP32 boards have a small blue
LED connected to pin 2:

```pycon
>>> from machine import Pin
>>> led = Pin(2, Pin.OUT)
>>> led.on()
>>> led.off()
```

The LED turns on and off as you type. You're controlling hardware with
Python!

!!! tip "Handy Shell shortcuts"
    - ++arrow-up++ brings back the previous line, so you don't have to
      retype it.
    - ++tab++ auto-completes names: type `led.o` and press Tab.

## Write a program in the editor

Typing into the Shell gets tedious for anything longer than a few lines.
In the editor (the big area at the top of Thonny), type this program:

```python title="blink.py"
--8<-- "lessons/led_builtin_blink.py"
```

Click the green **Run** button (or press ++f5++). Thonny asks where to save
the file: choose **This computer** and call it `blink.py`. The LED starts
blinking once a second.

While your program runs, the Shell has no `>>>`, because the board is busy.
To stop it, click the red **Stop** button (++ctrl+f2++).

### What just happened?

| Line | What it does |
|---|---|
| `import time` | Loads the `time` module so you can pause with `time.sleep()`. |
| `from machine import Pin` | Loads `Pin`, which is how you control the board's pins. |
| `led = Pin(2, Pin.OUT)` | Sets pin 2 up as an **output** and names it `led`. |
| `while True:` | Repeats the indented lines below it **forever**. |
| `led.on()` / `led.off()` | Turns pin 2's voltage on (3.3 V) or off (0 V). |
| `time.sleep(1)` | Waits 1 second. |

!!! info "Indentation matters"
    Python uses the spaces at the start of a line to know which lines
    belong to the `while` loop. Everything indented by 4 spaces under
    `while True:` repeats. Thonny indents automatically after a line
    ending in `:`.

## Try it yourself

- Change both `time.sleep(1)` lines to `time.sleep(0.1)`. How fast can you
  make it blink before it looks like it's always on?
- Make a heartbeat: two quick blinks, then a longer pause.

??? example "Show a heartbeat solution"

    ```python
    import time
    from machine import Pin

    led = Pin(2, Pin.OUT)

    while True:
        for beat in range(2):   # do this twice
            led.on()
            time.sleep(0.1)
            led.off()
            time.sleep(0.15)
        time.sleep(0.8)         # longer rest between heartbeats
    ```

**Next:** [Saving Programs to the Board](saving-programs.md)
