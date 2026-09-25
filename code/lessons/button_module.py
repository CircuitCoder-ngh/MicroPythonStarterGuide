# Count presses using the reusable Button class from button.py
# (copy button.py onto your ESP32 first)
from button import Button

button = Button(14)
presses = 0

while True:
    if button.was_pressed():
        presses += 1
        print("Pressed! Total:", presses)
