import numpy as np
import math

# inspiration
# https://github.com/wybiral/python-musical
# delay http://andrewslotnick.com/posts/audio-delay-with-python.html

# https://www.dsprelated.com/freebooks/pasp/Flanging.html
# linear interpolation
# https://www.dsprelated.com/freebooks/pasp/Delay_Line_Interpolation.html


def my_sine(f, len, rate=44100, phase=0.0):
    length = int(len * rate)
    t = np.arange(length) / float(rate)
    omega = 2 * math.pi * float(f)
    phase *= 2 * math.pi
    return np.sin(omega * t + phase)


def modulated_delay(data, modwave, dry, wet):
    # Use LFO "modwave" as a delay modulator (no feedback)
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = data[i] * dry + data[index] * wet
    return out


def feedback_modulated_delay(data, modwave, dry, wet):
    # Use LFO "modwave" as a delay modulator (with feedback)
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = out[i] * dry + out[index] * wet
    return out


def chorus(data, freq, dry=0.5, wet=0.5, depth=1.0, delay=25.0, rate=44100):
    # Chorus effect
    # http://en.wikipedia.org/wiki/Chorus_effect
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (my_sine(freq, length) / 2 + 0.5) * depth + delay
    return modulated_delay(data, modwave, dry, wet)


def flanger(data, freq, dry=0.5, wet=0.5, depth=20.0, delay=1.0, rate=44100):
    # Flanger effect
    # http://en.wikipedia.org/wiki/Flanging
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (my_sine(freq, length) / 2 + 0.5) * depth + delay
    return feedback_modulated_delay(data, modwave, dry, wet)


def tremolo(data, freq, dry=0.5, wet=0.5, rate=44100):
    # Tremolo effect
    # http://en.wikipedia.org/wiki/Tremolo

    length = float(len(data)) / rate
    modwave = (my_sine(freq, length) / 2 + 0.5)
    return (data * dry) + ((data * modwave) * wet)
