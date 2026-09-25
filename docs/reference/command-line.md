# Command-Line Tools

Thonny does everything this guide needs. If you prefer a terminal, or want to
use a different editor such as VS Code, these are the official tools that
Thonny uses behind the scenes.

## Install

You'll need Python 3 installed on your computer. Then:

```bash
pip install esptool mpremote
```

!!! tip "Use a virtual environment"
    It's good practice to install tools into a project's own virtual
    environment:

    === "Windows"

        ```bat
        py -m venv .venv
        .venv\Scripts\activate
        pip install esptool mpremote
        ```

    === "macOS / Linux"

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        pip install esptool mpremote
        ```

## esptool: flash MicroPython

Download the latest **ESP32_GENERIC** firmware (`.bin` file) from
[micropython.org](https://micropython.org/download/ESP32_GENERIC/), then:

```bash
esptool erase-flash
esptool --baud 460800 write-flash 0x1000 ESP32_GENERIC-xxxxxxxx-v1.xx.bin
```

- `erase-flash` wipes the board completely, including any files on it.
- `0x1000` is where the classic ESP32 expects its firmware to start.
  (Other ESP32 chips use different addresses; check the download page.)
- If esptool picks the wrong board, add `--port COM3` (Windows) or
  `--port /dev/ttyUSB0` (Linux) or `--port /dev/cu.usbserial-XXXX` (macOS)
  before the command.

!!! note "Older tutorials"
    esptool version 5 renamed its commands with dashes (`erase-flash`,
    `write-flash`) and is run as `esptool` rather than `esptool.py`. The
    old names still work for now, but show a warning.

## mpremote: run code and manage files

`mpremote` connects to the first board it finds.

| Task | Command |
|---|---|
| Open the REPL (exit with ++ctrl+x++) | `mpremote` |
| Run a file from your computer without saving it | `mpremote run blink.py` |
| Copy a file to the board | `mpremote cp button.py :` |
| Copy your program so it runs at power-up | `mpremote cp blink.py :main.py` |
| List files on the board | `mpremote ls` |
| Delete a file on the board | `mpremote rm :main.py` |
| Install a library from micropython-lib | `mpremote mip install ssd1306` |
| Reset the board | `mpremote reset` |

The `:` means "on the board". You can chain commands, for example
`mpremote cp button.py : + cp snake.py :main.py + reset`.

Full documentation: [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html).

!!! note "Coming from the first edition?"
    The original guide used `rshell` and the Python IDLE editor. `mpremote`
    is now the official tool and does everything `rshell` did.
