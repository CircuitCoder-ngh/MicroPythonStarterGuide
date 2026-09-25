# Install Thonny & MicroPython

You'll use one free program, **Thonny**, for everything in this guide. It's
a simple code editor made for beginners that can also load MicroPython
onto your board and run code on it.

## Step 1: Install Thonny

Download Thonny from **[thonny.org](https://thonny.org)** and run the
installer. It works on Windows, macOS and Linux, and comes with Python
built in, so there's nothing else to install.

## Step 2: Plug in your board

Connect the ESP32 to your computer with the USB cable. A small red power
light on the board should turn on.

Your computer talks to the board through a small **USB-to-serial chip**
next to the USB socket. It's usually a **CP2102** (a square chip) or a
**CH340** (a rectangular one). Windows 10/11, macOS and Linux include
drivers for both of these, so it normally just works.

??? question "My computer doesn't see the board"
    1. **Try a different USB cable.** Many cables only carry power, not
       data. This is the most common problem by far.
    2. Try a different USB port, and avoid USB hubs.
    3. Install the driver for your board's chip:
       [CP210x driver (Silicon Labs)](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
       or [CH340 driver (WCH)](https://www.wch-ic.com/downloads/CH341SER_EXE.html).
       Then unplug the board and plug it back in.

## Step 3: Put MicroPython on the board

A new ESP32 doesn't know Python yet. You need to **flash** (install) the
MicroPython firmware onto it once. After that, it stays there, even when
the board is unplugged.

=== "With Thonny (recommended)"

    1. In Thonny, open **Tools → Options…** and go to the **Interpreter** tab.
    2. In the first drop-down, choose **MicroPython (ESP32)**.
    3. Click **Install or update MicroPython (esptool)** in the bottom-right
       corner.
    4. In the window that opens:
        - **Target port:** your board, usually labelled *CP210x* or
          *USB-SERIAL CH340* (`COM3` or similar on Windows, `/dev/ttyUSB0`
          or `/dev/cu.usbserial-…` on Linux and macOS).
        - **MicroPython family:** `ESP32`
        - **Variant:** `Espressif • ESP32 / WROOM`
        - **Version:** the newest one offered
    5. Click **Install** and wait for it to reach *Done!* (about a minute).
    6. Close the window, make sure the same port is selected under
       **Port or WebREPL**, and click **OK**.

    !!! tip "Stuck on *Connecting…*?"
        Some boards need a nudge to accept new firmware. Hold down the
        **BOOT** button on the board (sometimes labelled **IO0**), click
        **Install**, and let go once the progress bar starts moving.

    Thonny's menus change a little between versions. If a label doesn't
    match exactly, look for the option with the closest name.

=== "With the command line"

    If you'd rather use a terminal, install
    [esptool](https://docs.espressif.com/projects/esptool/) with pip, then
    download the latest **ESP32_GENERIC** `.bin` file from
    [micropython.org/download/ESP32_GENERIC](https://micropython.org/download/ESP32_GENERIC/)
    (pick a release, not a *preview*).

    ```bash
    pip install esptool
    esptool erase-flash
    esptool --baud 460800 write-flash 0x1000 ESP32_GENERIC-xxxxxxxx-v1.xx.bin
    ```

    esptool finds your board automatically. If you have more than one, add
    `--port COM3` (or your port name). See
    [Command-Line Tools](../reference/command-line.md) for more.

## Step 4: Check it worked

At the bottom of Thonny is the **Shell**. After a moment it should show
something like:

```text
MicroPython v1.29.0 on 2026-08-24; Generic ESP32 module with ESP32
Type "help()" for more information.
>>>
```

The `>>>` means the board is ready for your commands. That's the
**REPL**, and you'll use it in the next step.

!!! question "No `>>>`?"
    Click the red **Stop** button (or press ++ctrl+f2++) to restart the
    connection. If that doesn't help, see
    [Troubleshooting](../reference/troubleshooting.md).

**Next:** [Your First Program](first-program.md)
