# Functions

A **function** is a named block of code that you can run whenever you want
by **calling** its name. You've already used plenty: `print()`, `len()`,
`time.sleep()`. Now you'll write your own.

## Defining a function

Use `def`, a name, brackets, and a colon. The indented code underneath is
the function's **body**:

```python
def say_hello():
    print("Hello!")
    print("Nice to meet you.")

say_hello()     # runs both print lines
say_hello()     # and again
```

Defining a function doesn't run it. Only calling it, with the brackets,
does.

## Parameters: giving a function information

Put names inside the brackets to let the function accept values:

```python
def blink(times, delay):
    for i in range(times):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

blink(3, 0.5)    # three slow blinks
blink(10, 0.05)  # ten fast blinks
```

## return: getting an answer back

`return` sends a value back to wherever the function was called:

```python
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

print(celsius_to_fahrenheit(20))   # 68.0
```

A really useful one for hardware is a function that **scales** a value from
one range to another. For example, it can turn a knob's reading (0–65535)
into an angle (0–180):

```python
def scale(value, in_min, in_max, out_min, out_max):
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)

scale(32768, 0, 65535, 0, 180)   # about 90.0
```

## Why bother with functions?

- **Less repetition.** Write the code once, and call it from anywhere.
- **Easier to read.** `update_display()` says what's happening much more
  clearly than 20 lines of drawing code in the middle of your main loop.
- **Easier to fix.** If something's wrong, there's only one place to
  change it.

The projects in this guide are planned exactly this way: decide what the
program needs to do, write a function for each job, and then call those
functions from the main loop.

## Variables inside functions

A variable created inside a function only exists **inside** that function.
To change a variable from the main program, declare it `global` first:

```python
score = 0

def add_point():
    global score     # "I mean the score from outside this function"
    score += 1

add_point()
print(score)   # 1
```

Without the `global` line, Python would give an error, because it would
think you meant a brand-new `score` inside the function.

## Modules: functions in another file

A **module** is a `.py` file full of functions (and other code) that you
can `import`. `time` and `machine` are modules built into MicroPython. You
can also put your own modules on the board. The lessons use a few, such as
`button.py`, which handles buttons for you:

```python
from button import Button

jump_button = Button(14)
```

That's all the Python you need to get going. Time to plug some things in!

[Start with Components :material-arrow-right:](../components/index.md){ .md-button .md-button--primary }
