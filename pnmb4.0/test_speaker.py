from utime import sleep
from machine import Pin, PWM
from speaker import (
    play_song,
    tones,
    hold_tone,
    be_quiet,
    min_frequency,
    max_frequency,
    warn,
    warn_by_time_between_beeps,
)

speaker_out = PWM(Pin(22))

song = [
    "E5",
    "G5",
    "A5",
    "P",
    "E5",
    "G5",
    "B5",
    "A5",
    "P",
    "E5",
    "G5",
    "A5",
    "P",
    "G5",
    "E5",
]

siren = [
    "FS5",
    "C6",
    "FS5",
    "C6",
    "FS5",
    "C6",
    "FS5",
    "C6",
    "FS5",
    "C6",
    "FS5",
    "C6",
    "FS5",
    "C6",
    "FS5",
    "C6",
    "FS5",
    "C6",
]

# play_song(speaker_out, song)

# play_song(speaker_out, siren, 0.1)

# play_song(speaker_out, siren, 0.4)

# play_song(speaker_out, [k for k in tones.keys()])

for frequency in range(min_frequency, max_frequency):
    hold_tone(speaker_out, frequency, 0.0001)

for severity in range(1, 11):
    print(f"Warning at severity level {severity}")
    warn(speaker_out, severity)
    sleep(1)
    warn_by_time_between_beeps(speaker_out, severity)
    sleep(1)

be_quiet(speaker_out)
