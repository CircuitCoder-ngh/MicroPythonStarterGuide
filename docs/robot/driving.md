# First Drive

<img src="../../assets/img/icons/robot.svg" alt="" class="cc-icon">

Your robot is built and both wheels spin the right way. Now let's drive! In
this lesson you'll meet the `robot.py` library, which turns "set four PWM
pins" into simple commands like `robot.forward()`. Then you'll drive in a
square and program a dance.

<div class="cc-parts" markdown>
**You'll need:**

- [x] Your assembled robot (see [Build the Robot](build.md))
- [x] `robot.py` saved on the ESP32
- [x] Some floor space, away from stairs!
</div>

## The robot library

[`robot.py`](https://github.com/CircuitCoder-ngh/MicroPythonStarterGuide/blob/main/code/lib/robot.py)
contains two **classes**. A class is a blueprint for an object that bundles
up some data with the functions that work on it. You've already used
classes like `Pin` and `Button`.

??? info "robot.py"

    ```python title="robot.py"
    --8<-- "lib/robot.py"
    ```

**`Motor`** controls one motor through two driver pins, using the same idea
as `set_motor()` in the [DC Motors](dc-motors.md) lesson, with one
improvement: it **maps** speeds 1–100 onto 35–100 % power. Remember how the
motor only hummed below about a third of full power? With this mapping,
`set_speed(1)` means "as slow as possible while still moving", so every
speed you ask for actually does something.

**`Robot`** creates two `Motor` objects, one per wheel, and gives you these
commands. All speeds are percentages from 0 to 100:

| Command | What the wheels do | What the robot does |
|---|---|---|
| `robot.forward(speed)` | Both forwards | Drives forwards |
| `robot.backward(speed)` | Both backwards | Reverses |
| `robot.spin_left(speed)` | Left backwards, right forwards | Turns left on the spot |
| `robot.spin_right(speed)` | Left forwards, right backwards | Turns right on the spot |
| `robot.drive(left, right)` | Each wheel set separately, -100 to 100 | Anything! |
| `robot.stop()` | Both off | Stops |

`drive()` is the one that does all the work. Every other command is just a
shortcut for it. For example, `drive(60, 30)` makes the left wheel faster
than the right, so the robot curves to the **right**.

## Your first drive

Put the robot on the floor, switch the battery pack on, and run:

```python title="drive_forward.py"
--8<-- "robot/drive_forward.py"
```

The three-second pause at the start gives you time to unplug the USB cable
and put the robot down. Or swap to the power bank, save the program as
`main.py`, and press the ESP32's **EN** button to start it.

!!! tip "The untethered workflow"
    1. With the USB cable plugged in, save your program to the board as
       `main.py`.
    2. Unplug the USB cable and plug in the power bank.
       The ESP32 restarts and runs `main.py`.
    3. To try again, press the ESP32's **EN** (reset) button.

## Drive in a square

Driving in a square is four times "go straight, then turn 90°". There's no
compass on the robot, so it doesn't know how far it has turned. It only
knows **how long** it has been turning. That's called **time-based**
driving.

```python title="drive_square.py"
--8<-- "robot/drive_square.py"
```

- `drive_for()` sets the wheels, waits, then stops and pauses. Stopping
  between moves makes each turn more consistent, because the robot starts
  every move from standstill.
- `TURN_MS_90` is how long a 90° spin takes. It depends on your motors,
  your batteries and even the floor, so **you have to tune it**: if the
  robot turns too far, make it smaller; not far enough, make it bigger.

### Why it doesn't come back to exactly where it started

However carefully you tune it, your square won't be perfect. That's normal,
and it's one of the big challenges in robotics:

- **No two motors are identical.** One is always a little faster, so the
  robot drifts to one side when "driving straight".
- **Batteries run down,** so everything gets slower over time, and your
  carefully tuned turns come up short.
- **Wheels slip,** especially on smooth floors or carpet.

You can correct the drift with the **`TRIM`** setting at the top of
`robot.py`. If the robot curves to the right, the left motor is faster, so
set `TRIM = 5` (or so) to slow it down. Curving left? Try `TRIM = -5`.
Adjust until it drives straight for a metre or two.

Real robots solve these problems with **sensors**: wheel encoders that count
how far each wheel has turned, compasses and gyroscopes that measure the
heading. For our robot, the sensors in the next few lessons let it react to
the world instead of driving blind.

!!! tip "A wheel turns the wrong way?"
    If you swapped motors or wires since the wheel test, you can fix the
    direction in code instead of rewiring: set `LEFT_INVERT` or
    `RIGHT_INVERT` to `True` at the top of `robot.py`.

## Challenge: make it dance

A dance is just a list of moves played back in order. Each move could be a
`(left speed, right speed, milliseconds)` tuple. Write a program that plays
through a list like this, and choreograph your own routine!

??? example "Show a solution"

    ```python title="dance.py"
    --8<-- "robot/dance.py"
    ```

    Storing the moves as **data** in a list, separate from the code that plays
    them, makes it easy to write new routines without touching the loop.
    Try adding the buzzer from the [Buzzers](../components/buzzers.md)
    lesson so it plays a note with each move.

**Next up:** give your robot eyes. [Obstacle Avoider](obstacle-avoider.md).
