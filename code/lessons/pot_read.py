# Read a potentiometer and print the value twice a second
import time
from machine import ADC, Pin

POT_PIN = 34  # use an ADC1 pin (32-39) so it still works with Wi-Fi on

# ATTN_11DB lets the pin measure the full 0-3.3 V range
pot = ADC(Pin(POT_PIN), atten=ADC.ATTN_11DB)

while True:
    raw = pot.read_u16()             # 0 (0 V) up to 65535 (3.3 V)
    percent = raw * 100 // 65535     # scale to 0-100
    print("raw:", raw, "  percent:", percent)
    time.sleep(0.5)
