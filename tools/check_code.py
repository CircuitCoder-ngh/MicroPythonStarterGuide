"""Sanity checks for the MicroPython code in code/.

Runs in CI before the site is built. It can't run the code on real
hardware, but it catches syntax errors and APIs that no longer work on
current ESP32 MicroPython firmware.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "code"

# (pattern, why it's banned)
OUTDATED = [
    (r"Timer\(\s*-1\s*\)", "virtual timers (Timer(-1)) aren't supported on ESP32; use button.py or ticks_ms()"),
    (r"\.duty\(", "use duty_u16() or duty_ns() instead of the legacy duty()"),
    (r"\.width\(", "ADC.width() is legacy; use read_u16()"),
    (r"\bADC\.WIDTH_", "ADC widths are legacy; use read_u16()"),
    (r"\.read\(\)\s*(#.*)?$", "ADC.read() is legacy; use read_u16()"),
    (r"\burequests\b", "import requests instead of urequests"),
    (r"\bSTA_IF\b|\bAP_IF\b", "use network.WLAN.IF_STA"),
    (r"\.ifconfig\(", "use wlan.ipconfig('addr4')"),
    (r"freq\s*=\s*0\b|\.freq\(\s*0\s*\)", "a PWM frequency of 0 is invalid; use deinit() or a duty of 0"),
    (r"worldtimeapi", "worldtimeapi.org is unreliable; use ntptime"),
    (r"ifttt", "IFTTT webhooks are paid-only now; use ntfy.sh"),
]

# Files we didn't write and shouldn't lint for style
SKIP = {"ssd1306.py"}


def main():
    problems = 0
    files = sorted(ROOT.rglob("*.py"))
    for path in files:
        source = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        try:
            compile(source, str(rel), "exec")
        except SyntaxError as err:
            print(f"{rel}:{err.lineno}: syntax error: {err.msg}")
            problems += 1
            continue
        if path.name in SKIP:
            continue
        for lineno, line in enumerate(source.splitlines(), 1):
            for pattern, reason in OUTDATED:
                if re.search(pattern, line):
                    print(f"{rel}:{lineno}: {reason}\n    {line.strip()}")
                    problems += 1
    print(f"Checked {len(files)} files, {problems} problem(s).")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
