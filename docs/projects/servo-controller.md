# Project: Servo Controller

<img src="../../assets/img/icons/servo.png" alt="" class="cc-icon">

Servo motors are what make robot arms, camera mounts and RC car steering
move. In this project you'll steer one yourself, in two different ways:
with a **dial** for fast, natural control, and with **two buttons** for
slow, precise control.

![Controlling a servo with a potentiometer](../assets/img/photos/servo-pot-2.jpg){ .cc-photo width="420" loading=lazy }

*Photo from the first edition. Follow the wiring table for pin numbers.*

## Objective

- **Version 1:** the servo arm follows the potentiometer. Turn the dial and
  the arm turns with it.
- **Version 2:** Button A turns the servo one way and Button B the other.
  Tap for a 1° nudge, or hold the button down to keep it moving.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × servo motor (SG90 or similar)
- [x] 1 × potentiometer (version 1)
- [x] 2 × push buttons (version 2)
- [x] Jumper wires
</div>

!!! note "Before you start"
    This project builds on [Servo Motors](../components/servos.md),
    [Potentiometers](../components/potentiometers.md) and
    [Buttons](../components/buttons.md). Version 2 needs **`button.py`** saved
    on your ESP32 (see [Saving Programs to the Board](../getting-started/saving-programs.md)).

## Wiring

You can wire up everything at once and switch between the two versions just
by running different code.

| Part | Wire / leg | Connects to |
|---|---|---|
| Servo | brown or black (ground) | **GND** |
| | red (power) | **VIN** (5 V) |
| | orange or yellow (signal) | GPIO **13** |
| Potentiometer 1 | left leg | **3V3** |
| | middle leg | GPIO **34** |
| | right leg | **GND** |
| Button A | one leg | GPIO **14**, other leg to **GND** |
| Button B | one leg | GPIO **25**, other leg to **GND** |

!!! warning "Power the servo from VIN, not 3V3"
    Servos want about 5 V and can draw a lot of current when they move. VIN
    passes 5 V straight through from USB. If your ESP32 resets whenever the
    servo moves, the USB port can't keep up. Try a different port or a
    powered USB hub.

## Plan it out

1. **Set up each component:** the servo is a PWM output at 50 Hz, the
   potentiometer is an ADC input, and the buttons use `Button` from
   `button.py`.
2. **Break the job into functions.**
    - `set_angle(angle)` turns an angle (0–180°) into the right pulse width
      for the servo. Both versions use it.
    - Version 1: `read_pot_angle()` turns the dial position into an angle.
    - Version 2: `move(step)` changes the angle by ±1° without going past 0
      or 180. `check_button()` decides whether a button was tapped or is
      being held.
3. **Main loop:** keep reading the input and move the servo to match.

## Code

=== "Version 1: Potentiometer"

    ```python title="servo_pot_control.py"
    --8<-- "projects/servo_pot_control.py"
    ```

=== "Version 2: Buttons"

    ```python title="servo_button_control.py"
    --8<-- "projects/servo_button_control.py"
    ```

Save whichever version you want to use as **`main.py`** on the ESP32 to
have it start automatically.

## How it works

### Angles and pulses

A servo decides where to point by measuring how long each pulse on its
signal wire lasts. There are 50 pulses a second, and:

| Pulse width | Angle |
|---|---|
| 0.5 ms (500,000 ns) | 0° |
| 1.5 ms (1,500,000 ns) | 90° |
| 2.5 ms (2,500,000 ns) | 180° |

`set_angle()` maps 0–180 onto `SERVO_MIN_NS`–`SERVO_MAX_NS` and hands the
result to `duty_ns()`. Every servo is a little different: if yours doesn't
quite reach the ends, or buzzes when it gets there, nudge those two
constants (try 600,000 and 2,400,000).

### Version 1: smoothing the dial

The ESP32's analog input is a bit noisy. Even when you aren't touching the
dial, the reading jumps around slightly, which would make the servo
twitch. The code fixes this in two ways:

- `read_pot_angle()` takes **8 readings and averages them**.
- The main loop only moves the servo when the angle has changed by at least
  one whole degree.

### Version 2: tap vs. hold

`Button.was_pressed()` is `True` just once per press. That's the 1° tap.
`Button.is_down()` is `True` the whole time the button is held down. Once
it's been held for `HOLD_DELAY_MS` (0.4 s), the code moves another degree
every `REPEAT_MS` (50 ms). This is exactly how the arrow keys on your
keyboard repeat.

`max(0, min(180, angle + step))` is a handy pattern called **clamping**:
whatever `angle + step` works out to, the result is kept between 0 and 180.

## Result

<div class="cc-gallery">
<img src="../../assets/img/photos/servo-pot-1.jpg" alt="Pot turned left" loading="lazy">
<img src="../../assets/img/photos/servo-pot-2.jpg" alt="Pot in the middle" loading="lazy">
<img src="../../assets/img/photos/servo-pot-3.jpg" alt="Pot turned right" loading="lazy">
</div>

<div class="cc-gallery">
<img src="../../assets/img/photos/servo-buttons-1.jpg" alt="Servo moved with the buttons" loading="lazy">
<img src="../../assets/img/photos/servo-buttons-2.jpg" alt="Pressing a button to turn the servo" loading="lazy">
</div>

*Photos from the first edition. Follow the wiring table for pin numbers.*

## Make it your own

- **Speed control:** in version 2, make the servo speed up the longer you
  hold the button.
- **Both at once:** combine the versions, using the dial for rough
  positioning and the buttons for fine-tuning.
- **Pan and tilt:** add a second servo on GPIO 27 controlled by
  Potentiometer 2 (GPIO 35), tape a small cardboard "camera" on top, and
  you've built a pan-and-tilt mount.
