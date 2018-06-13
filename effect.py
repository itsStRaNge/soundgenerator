import numpy as np
import math

# inspiration
# https://github.com/wybiral/python-musical
# delay http://andrewslotnick.com/posts/audio-delay-with-python.html

# https://www.dsprelated.com/freebooks/pasp/Flanging.html
# linear interpolation
# https://www.dsprelated.com/freebooks/pasp/Delay_Line_Interpolation.html

ms = 0.001


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


def flanger(data, dry=0.5, wet=0.5, delay=5, depth=2, rate=3, fs=44100):
    """
        delay in ms [0, 100]
        lfo rate in Hz ([0, 50])
        delay depth in ms (minimum of 0)
        feedback  [0, 1]
        dry/wet = ([0, 1])
    """

    # convert delays in ms to delay in samples
    delay = delay * fs / 10 ** 3
    depth = depth * fs / 10 ** 3

    # get delay in samples
    for i in range(0, len(data)):
        try:
            d = int(delay + depth * np.sin(rate * i/fs))
            data[i + d] = data[i + d] * dry + data[i] * wet
        except IndexError:
            break
    return data


def tremolo(data, freq, dry=0.5, wet=0.5, rate=44100):
    # Tremolo effect
    # http://en.wikipedia.org/wiki/Tremolo

    length = float(len(data)) / rate
    modwave = (my_sine(freq, length) / 2 + 0.5)
    return (data * dry) + ((data * modwave) * wet)
