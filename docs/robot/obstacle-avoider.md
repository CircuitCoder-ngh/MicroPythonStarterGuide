# Obstacle Avoider

<img src="../../assets/img/icons/ultrasonic.svg" alt="" class="cc-icon">

This is where your robot comes alive. Instead of following a script, it will
**sense** its surroundings and **decide** what to do by itself: drive
forwards, and when something gets in the way, back up and find another way
around. Set it loose in a room and watch it explore.

<div class="cc-parts" markdown>
**You'll need:**

- [x] Your robot, with the ultrasonic sensor at the front
- [x] 1 × push button (Button A) to start and stop it
- [x] Optional: the piezo buzzer, for a "beep!" when it spots something
- [x] `robot.py`, `button.py` and `distance.py` saved on the ESP32
</div>

## Sense, think, act

Almost every robot, from a robot vacuum to a self-driving car, runs the same
loop, over and over:

1. **Sense:** read the sensors. *How far away is the nearest thing in front
   of me?*
2. **Think:** decide what to do. *Is that too close?*
3. **Act:** drive the motors. *Keep going, or turn away.*

Our obstacle avoider does exactly this, dozens of times a second.

## Wiring

On top of the wiring from [Build the Robot](build.md), add:

| Part | Pin | Connects to |
|---|---|---|
| Button A | one leg | GPIO **14**, other leg to **GND** |
| Buzzer (optional) | + | GPIO **26**, other leg to **GND** |

The ultrasonic sensor is already wired to **GPIO 5** (TRIG) and **GPIO 39**
(ECHO). If you haven't used it before, the
[Ultrasonic Sensors](../components/ultrasonic.md) lesson explains how it
works.

## Plan it out

1. **Set up** the robot, the button, the distance sensor and the buzzer.
2. **Break it into functions:**
    - `chirp()` beeps the buzzer.
    - `avoid()` does the escape move: stop, beep, reverse a little, then spin
      left or right (picked at random) for a random amount of time.
3. **Main loop:**
    - If Button A was pressed, switch between running and stopped.
    - If running, measure the distance. Too close? `avoid()`. Otherwise,
      drive forwards.

!!! tip "Why a start button?"
    If the robot started driving the moment it powered up, it would shoot
    off the desk while you were still plugging in the power bank. The
    button means it waits until you're ready.

## Code

Save this to the ESP32 as **`main.py`**.

```python title="obstacle_avoider.py"
--8<-- "robot/obstacle_avoider.py"
```

## How it works

### "Nothing there" is not zero

`sensor.distance_cm()` returns `None` when no echo came back. That happens
when nothing is within range, or the sound bounced off at an angle and never
returned. So the check is:

```python
if distance is not None and distance < TOO_CLOSE_CM:
```

Checking for `None` first matters, because comparing `None < 20` would
crash the program.

### Why turn randomly?

If the robot always turned right, it could get stuck forever in a corner,
turning right into the other wall, then right again... Picking a random
direction and a random turn time (`random.randint(300, 700)` milliseconds)
means it will eventually wriggle its way out of almost anything. A lot of
simple robot vacuums use exactly this trick!

### Tuning

- **`CRUISE_SPEED`:** faster is more fun, but the robot needs time to stop.
  If it bumps into things before reacting, slow it down or raise
  `TOO_CLOSE_CM`.
- **`TOO_CLOSE_CM`:** 20 cm works for most rooms. Tight spaces might need
  less.

!!! warning "Blind spots"
    The ultrasonic sensor "sees" a cone about 30° wide straight ahead. It can
    miss thin things like chair legs, soft things like cushions and curtains
    (they absorb the sound), and walls it approaches at a steep angle (the
    echo bounces away). That's why real robots use several different kinds
    of sensor.

!!! note "Hold the button"
    While the robot is doing its escape move, the program isn't checking the
    button. If a quick tap doesn't stop it, hold the button down for a
    second.

## Level up: a scanning head

Right now the robot turns a random way when blocked. A smarter robot would
**look around first**, and turn towards whichever side is more open.

Mount the ultrasonic sensor on top of an **SG90 servo** (a small bracket,
double-sided tape or even a folded piece of card works), facing forwards
when the servo is at 90°. Connect the servo as in the
[Servo Motors](../components/servos.md) lesson: signal to **GPIO 13**, power
to **VIN**, ground to **GND**. If you've built the
[Sonar Radar](../projects/sonar-radar.md), it's the same scanner, now on
wheels!

```python title="obstacle_scanner.py"
--8<-- "robot/obstacle_scanner.py"
```

When something is in the way, `choose_new_direction()` backs up a little,
turns the servo to look left, then right, and measures the distance each
way with `look()`. The robot then spins towards the more open side. If both
sides are blocked, it turns right around.

!!! tip "Servo power"
    The servo is powered from the ESP32's VIN pin, which gets 5 V from the
    USB power bank. If the ESP32 restarts when the servo moves, your power
    bank may not be able to keep up. Try another one.

## Make it your own

- **Speed up when it's clear:** drive faster when the nearest obstacle is far
  away, and slow down smoothly as things get closer. (Hint: work out the speed
  from the distance.)
- **Headlights:** add the [NeoPixels](../components/neopixels.md) or an
  [RGB LED](../components/rgb-led.md) that glow green when the way is clear
  and red when it's reacting.
- **Explorer mode:** count how many obstacles it avoids and print the total
  when you stop it.
- **Edge detector:** point a line sensor down at the edge of a table and
  make the robot back away from drops. (Test this with a hand ready to catch
  it!)

**Next up:** [Line Follower](line-follower.md).
