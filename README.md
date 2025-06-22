# twelve-tone-midi
This Python script generates Schoenberg-style 12-tone rows and exports:
- Original row as MIDI
- Inversion, Retrograde, Retrograde Inversion as separate MIDI files
- Combined version as a single MIDI file
- Each run outputs to a timestamped folder to keep results organized

## Requirements

- Python 3.x
- midiutil (`pip install midiutil`)

## How to run

```bash
python twelve_tone_midi.py
