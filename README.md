# CircuitCoder: MicroPython Starter Guide

A free, hands-on guide to learning electronics and programming with an
**ESP32** and **MicroPython**. Learn how each component works, then combine
them into projects: a Snake game, a Wi-Fi alarm clock, a motion alert that
pings your phone, and more.

**Read the guide:** https://circuitcoder-ngh.github.io/MicroPythonStarterGuide/

## What's in this repo

| Folder | Contents |
|---|---|
| `code/lessons/` | Short example for each component lesson |
| `code/projects/` | Full project programs; save one to your board as `main.py` |
| `code/robot/` | Programs for the two-wheeled robot: motor tests, driving, obstacle avoider, line follower, Wi-Fi remote control |
| `code/lib/` | Library files to copy onto your board: `button.py`, `distance.py`, `robot.py`, `wifi.py`, `ssd1306.py`, and `secrets_example.py` (copy it as `secrets.py`) |
| `docs/` | The website source (Markdown, built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)) |
| `tools/` | `check_code.py`, a CI check that catches syntax errors and outdated MicroPython APIs |
| `legacy/` | The original 2021 edition, kept for reference |

## Working on the site

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve                     # live preview at http://127.0.0.1:8000
```

Every push to `main` checks the code, builds the site, and publishes it to
GitHub Pages (see `.github/workflows/deploy.yml`).

## Second edition (2026)

This edition modernises the original 2021 guide:

- **Thonny** replaces the venv + `rshell` + IDLE setup, and firmware is flashed
  from inside Thonny.
- The code is updated for current MicroPython (v1.2x). Virtual timers
  (`Timer(-1)`) no longer exist on the ESP32, so buttons now use a small
  debounced `Button` class.
- It uses the current `PWM.duty_u16()`/`duty_ns()`, `ADC.read_u16()`, `requests`
  and `network.WLAN.IF_STA` APIs.
- The worldtimeapi.org clock is replaced with NTP, and the IFTTT email alert
  with free [ntfy.sh](https://ntfy.sh) push notifications.
- The fixes include current-limiting resistors on LEDs, the swapped I2C pin
  labels, ADC2 pins that don't work with Wi-Fi, and several code bugs.
