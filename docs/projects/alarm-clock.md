# Project: Alarm Clock

<img src="../../assets/img/icons/wifi.png" alt="" class="cc-icon">

The capstone project brings together nearly everything you've learned:
buttons, a buzzer, the OLED screen, Wi-Fi, and a program with several
"modes". You'll build a clock that sets itself from the internet, with an
alarm, a stopwatch and a countdown timer.

![The finished alarm clock](../assets/img/photos/alarm-clock-1.jpg){ .cc-photo width="380" loading=lazy }

*Photo from the first edition. Follow the wiring table for pin numbers.*

## Objective

The clock has four **pages**. Buttons A and C flip between them, and Button
B does something different on each one:

| Page | What it shows | What Button **B** does |
|---|---|---|
| **Clock** | Date, time, and whether the alarm is set | Turns the alarm on or off |
| **Set Alarm** | The alarm time | Edit → hours → minutes → save (A/C change the number) |
| **Stopwatch** | Minutes, seconds and tenths | Start → stop → reset |
| **Timer** | A countdown | Edit → minutes → seconds → start (press again to cancel) |

When the alarm or timer goes off, the buzzer beeps until you press **any**
button.

<div class="cc-parts" markdown>
**You'll need:**

- [x] 1 × SSD1306 OLED screen (128 × 64, I2C)
- [x] 3 × push buttons
- [x] 1 × passive piezo buzzer
- [x] A 2.4 GHz Wi-Fi network
- [x] Jumper wires
</div>

!!! note "Before you start"
    This project builds on [OLED Screens](../components/oled.md),
    [Buttons](../components/buttons.md), [Piezo Buzzers](../components/buzzers.md)
    and [Wi-Fi & APIs](../components/wifi.md). Make sure **`button.py`**,
    **`ssd1306.py`**, **`wifi.py`** and your **`secrets.py`** are saved on your
    ESP32 (see [Saving Programs to the Board](../getting-started/saving-programs.md)).

## Wiring

| Part | Pin | Connects to |
|---|---|---|
| OLED | GND | **GND** |
| | VCC | **3V3** |
| | SCL | GPIO **22** |
| | SDA | GPIO **21** |
| Button A (previous) | one leg | GPIO **14**, other leg to **GND** |
| Button B (select) | one leg | GPIO **25**, other leg to **GND** |
| Button C (next) | one leg | GPIO **32**, other leg to **GND** |
| Buzzer | + leg | GPIO **26** |
| | – leg | **GND** |

Line the buttons up **A – B – C** from left to right, so the outside two
act like arrows and the middle one like "OK".

## Set your time zone

The ESP32 gets the time from an internet **time server** using NTP
(Network Time Protocol). Time servers always give **UTC**, the time in
London in winter, so you need to tell the clock how far your time zone is
from UTC. Add this line to your `secrets.py`:

```python title="secrets.py"
UTC_OFFSET_HOURS = -5   # New York in winter. Use -4 in summer.
```

Some examples: Los Angeles `-8` (summer `-7`), Chicago `-6` (`-5`),
London `0` (`1`), Berlin `1` (`2`), India `5.5`, Sydney `10` (`11` in
their summer).

!!! info "About daylight saving time"
    This clock doesn't know about daylight saving time. The rules differ in
    every country and change over the years. When your clocks go forward
    or back, update `UTC_OFFSET_HOURS` in `secrets.py`. (Making the clock
    handle DST automatically is a great challenge if you want one!)

## Plan it out

This is the biggest program in the guide, so planning really pays off.

1. **Set up the components** (three buttons, buzzer and screen), then
   connect to Wi-Fi and set the clock.
2. **Keep track of the state.** Instead of lots of separate loops, the
   program has one main loop and a handful of variables that describe
   what's going on right now: which `page` you're on, what you're
   `editing`, whether the stopwatch or timer is running, and whether the
   buzzer is `ringing`.
3. **Break the job into functions.**
    - `press_select()` and `press_arrow()` decide what a button press means
      on the current page.
    - `check_alarm()` and `check_timer()` start the buzzer at the right time.
    - `update_buzzer()` beeps on and off while ringing.
    - `draw()` draws the current page.
4. **Main loop:** check buttons → check alarm and timer → update buzzer →
   redraw the screen, about 200 times a second.

## Code

Save this to your ESP32 as **`main.py`** so your clock starts whenever it's
plugged in.

```python title="alarm_clock.py"
--8<-- "projects/alarm_clock.py"
```

## How it works

### Getting the time

`ntptime.settime()` asks a time server for the current time and sets the
ESP32's internal clock (its *RTC*) to UTC. From then on, `time.time()`
counts the seconds by itself, even without Wi-Fi. The clock drifts by a
few seconds a day, so the main loop re-syncs once an hour.

`local_time()` adds your offset and splits the result into parts with
`time.localtime()`:

```python
(year, month, day, hour, minute, second, weekday, yearday)
```

so `now[3]` is the hour, `now[4]` the minute, and so on.

### One loop, many modes

The first edition used a separate `while True` loop for every mode. That
got complicated, and while one loop ran, nothing else could happen: the
alarm couldn't ring while you were using the stopwatch.

This version uses a **state machine**. There's only **one** loop, and
variables like `page`, `editing` and `timer_running` remember what
mode the clock is in. Each button press just *changes those variables*.
Look at `press_select()` on the Set Alarm page:

```python
if editing is None:
    editing = "hour"        # 1st press: start editing the hour
elif editing == "hour":
    editing = "minute"      # 2nd press: move on to the minutes
else:
    editing = None          # 3rd press: save
```

Because the loop never gets stuck, the alarm, timer and stopwatch all keep
working no matter which page you're looking at.

### Wrapping numbers with `%`

`(alarm_hour + change) % 24` keeps the hour between 0 and 23: going up from
23 gives `24 % 24 = 0`, and going down from 0 gives `-1 % 24 = 23`. Minutes
and seconds wrap the same way with `% 60`.

### Making the alarm ring only once

The alarm checks whether the current hour and minute match. But that stays
true for a whole minute, so after you silence it, it would start ringing
again straight away! `alarm_done` remembers the `(day, hour, minute)` the
alarm last rang, and it won't ring twice for the same one.

## Result

<div class="cc-gallery">
<img src="../../assets/img/photos/alarm-clock-1.jpg" alt="Alarm clock showing the time" loading="lazy">
<img src="../../assets/img/photos/alarm-clock-2.jpg" alt="Alarm clock circuit with three buttons and a buzzer" loading="lazy">
</div>

*Photos from the first edition. Follow the wiring table for pin numbers.*

## Make it your own

- **Snooze:** make Button B silence the alarm for 5 minutes, and only A or
  C turn it off for good.
- **Big digits:** the built-in font is only 8 pixels tall. Draw your own
  large numbers with `display.fill_rect()` so the time is readable from
  across the room.
- **Weather page:** add a fifth page that shows the temperature, fetched
  from a free weather API such as [Open-Meteo](https://open-meteo.com) (see
  [Wi-Fi & APIs](../components/wifi.md) for how to make the request).
- **Sunrise light:** add an LED that fades up over the 10 minutes before
  the alarm, using PWM.
