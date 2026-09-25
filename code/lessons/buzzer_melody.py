# Play "Twinkle Twinkle Little Star"
import time
from machine import PWM, Pin

BUZZER_PIN = 26
BEAT = 0.3  # seconds per beat: smaller is faster

# Frequency (Hz) of each note in the middle octave
NOTES = {
    "C": 262, "D": 294, "E": 330, "F": 349,
    "G": 392, "A": 440, "B": 494, "C5": 523,
}

# Each item is (note, number of beats). "-" is a rest (silence).
SONG = [
    ("C", 1), ("C", 1), ("G", 1), ("G", 1), ("A", 1), ("A", 1), ("G", 2),
    ("F", 1), ("F", 1), ("E", 1), ("E", 1), ("D", 1), ("D", 1), ("C", 2),
]

buzzer = PWM(Pin(BUZZER_PIN), freq=440, duty_u16=0)


def play(note, beats):
    if note == "-":
        buzzer.duty_u16(0)
    else:
        buzzer.freq(NOTES[note])
        buzzer.duty_u16(32768)
    time.sleep(BEAT * beats * 0.9)
    buzzer.duty_u16(0)            # a tiny gap so repeated notes sound separate
    time.sleep(BEAT * beats * 0.1)


for note, beats in SONG:
    play(note, beats)

buzzer.deinit()
