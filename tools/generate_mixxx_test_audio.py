"""Create clearly labelled calibration WAVs for native renderer checks (not music)."""
import argparse
import array
import math
from pathlib import Path
import wave


def generate(destination):
    destination.mkdir(parents=True, exist_ok=True)
    sample_rate = 22050
    for bpm in (120, 128, 124, 132):
        samples = array.array('h')
        for index in range(sample_rate * 32):
            seconds = index / sample_rate
            beat = seconds * bpm / 60
            phase = beat % 1
            bar = int(beat // 4) % 4
            low = .58 * math.sin(2 * math.pi * 60 * seconds) * math.exp(-phase * 24)
            mid = .19 * math.sin(2 * math.pi * (450 + bar * 170) * seconds) * math.exp(-(beat % .5) * 9)
            high = .13 * math.sin(2 * math.pi * 6500 * seconds) * math.exp(-(beat % .25) * 60)
            value = int(max(-.98, min(.98, low + mid + high)) * 32767)
            samples.extend((value, value))
        import sys
        if sys.byteorder != 'little':
            samples.byteswap()
        path = destination / f'SYNTHETIC - Three band check - {bpm} BPM.wav'
        with wave.open(str(path), 'w') as output:
            output.setparams((2, 2, sample_rate, 0, 'NONE', 'not compressed'))
            output.writeframes(samples.tobytes())
        print(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_directory', type=Path)
    generate(parser.parse_args().output_directory)
