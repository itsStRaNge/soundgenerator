import numpy as np
import math

# inspiration
# https://github.com/wybiral/python-musical
# delay http://andrewslotnick.com/posts/audio-delay-with-python.html

# https://www.dsprelated.com/freebooks/pasp/Flanging.html
# linear interpolation
# https://www.dsprelated.com/freebooks/pasp/Delay_Line_Interpolation.html


def flanger(data, dry=0.5, wet=0.5, delay=20, depth=20, rate=.3, fs=44100):
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

    # apply flanger effect
    output = np.zeros(data.shape)
    a = 2 * np.pi * rate
    for i in range(0, len(data)):
        try:
            d = i - int(delay + depth * np.sin(a * i/fs))
            if d < 0:
                d = i
            output[i] = data[d] * dry + data[i] * wet
        except IndexError:
            break
    return output


def tremolo(data, dry=0.5, wet=0.5, rate=2.0, fs=44100):
    """
        rate [0.0, 20.0]
    """
    t = np.linspace(0, len(data) / fs, len(data))
    modwave = np.sin(2 * np.pi * rate * t) / 2 + 0.5
    return (data * dry) + ((data * modwave) * wet)
