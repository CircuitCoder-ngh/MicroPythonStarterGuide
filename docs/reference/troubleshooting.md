# Troubleshooting

Something not working? Start here. Most problems come down to a handful of
causes.

## Connecting to the board

??? question "Thonny can't find my board / no port is listed"
    1. **Swap the USB cable.** Charge-only cables are the number-one cause.
    2. Try another USB port directly on the computer, not a hub.
    3. Install the USB driver for your board's chip. See
       [Setup, step 2](../getting-started/setup.md#step-2-plug-in-your-board).
    4. Unplug the board, wait a few seconds, plug it back in, then choose the
       port again under **Tools → Options → Interpreter**.

??? question "*Could not enter REPL* or *Device is busy*"
    A program on the board is running and not listening. Click **Stop**
    (++ctrl+f2++) a couple of times. If `main.py` starts up so quickly that
    Thonny can't get in, press the board's **EN/RST** button and then
    immediately click **Stop**.

??? question "Another program is using the port"
    Only one program can talk to the board at a time. Close the Arduino IDE,
    any other Thonny window, or serial monitor apps.

??? question "Flashing is stuck on *Connecting…*"
    Hold down the **BOOT** (IO0) button on the board while flashing starts,
    and let go once the progress bar moves.

## Errors in the Shell

The **last line** of an error message tells you what went wrong, and the
lines above it tell you where (`line 12` and so on).

| Error | What it usually means |
|---|---|
| `ImportError: no module named 'ssd1306'` | A library file isn't on the board. Upload it; see [Copy library files to the board](../getting-started/saving-programs.md#copy-library-files-to-the-board). The same goes for `button`, `wifi` and `secrets`. |
| `NameError: name 'led' isn't defined` | A typo in a variable name, or using a variable before the line that creates it. Remember names are case-sensitive. |
| `IndentationError` | The spaces at the start of a line are wrong. Code inside `if`, `for`, `while` and `def` must be indented by 4 spaces. |
| `SyntaxError` | Python can't read the line: often a missing `:`, bracket or quote on that line *or the one above*. |
| `ValueError: invalid pin` | That GPIO number can't be used for what you asked. See [ESP32 Pins](esp32-pins.md). |
| `OSError: [Errno 19] ENODEV` (screen) | The ESP32 can't find the OLED. Check the SDA/SCL wires (21 and 22) and that VCC goes to 3V3. |
| `OSError: -202` (Wi-Fi) | No internet connection, or the web address couldn't be found. Check Wi-Fi first. |
| `MemoryError` | The program ran out of memory. Close web responses with `response.close()` and avoid growing lists forever. |

## Circuits

??? question "My LED doesn't light up"
    - Is it the right way round? The **long leg** goes towards the pin, the
      short leg towards GND.
    - Is the resistor in the same breadboard row as the LED leg it connects
      to?
    - Test the LED with the pin forced on in the Shell:
      `Pin(27, Pin.OUT).on()`.

??? question "My button always reads the same value"
    - Buttons have 4 legs in two joined pairs. Put the button across the
      breadboard's centre channel, and use two legs on the **same side**.
    - Make sure the code uses `Pin.PULL_UP` (the `Button` class does this for
      you).
    - GPIO 34–39 don't have pull-up resistors, so don't use them for
      buttons.

??? question "My servo twitches, or the board resets when the servo moves"
    Servos draw bursts of current. Power the servo from **VIN** (5 V), not
    3V3. Use a short, good-quality USB cable, and plug into a computer port
    or a phone charger rather than a hub.

??? question "My potentiometer readings jump around"
    A small amount of jitter is normal. Average several readings (the
    [potentiometer lesson](../components/potentiometers.md) shows how), and
    make sure you're using an ADC1 pin (32–39), especially with Wi-Fi on.

??? question "The board keeps restarting (brownout)"
    If the Shell shows *Brownout detector was triggered*, the board isn't
    getting enough power, usually because a servo or other motor is drawing
    too much. Try another USB cable or port, or power the motor separately.

## Still stuck?

Search the [MicroPython forum](https://github.com/orgs/micropython/discussions)
for your error message. Chances are someone has hit the same thing before.
You can also [open an issue](https://github.com/CircuitCoder-ngh/MicroPythonStarterGuide/issues)
on this guide's GitHub page.
