import numpy as np


def reverb(data, g=0.5, m=10, fs=44100):
    # convert m from ms to samples
    m = int(m * fs / 10 ** 3)

    y = np.zeros(data.shape)

    for i in range(0, len(data)):
        if i-m < 0:
            y[i] = data[i]
        else:
            y[i] = -g * data[i] + data[i-m] + g * y[i-m]

    return y


def distortion(data, gain=75, dry=0.5, wet=0.5):
    """
        gain [0, inf] | don't know upper bound yet, but something around 200 seems good
    """
    abs_data = np.abs(data)
    max_data = np.max(abs_data)

    q = data * gain / max_data
    v = np.multiply(np.sign(-q), q)
    p = 1 - np.exp(v)
    z = np.multiply(np.sign(-q), p)
    y = dry * data + wet * z * max_data / np.max(np.abs(z))
    return y * max_data / np.max(np.abs(y))


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
    y = np.zeros(data.shape)
    a = 2 * np.pi * rate / fs
    for i in range(0, len(data)):
        d = i - int(delay + depth * np.sin(a * i))
        if d < 0:
            d = i
        y[i] = data[i] * dry + data[d] * wet
    return y


def tremolo(data, dry=0.5, wet=0.5, rate=2.0, fs=44100):
    """
        rate [0.0, 20.0]
    """
    t = np.linspace(0, len(data) / fs, len(data))
    modwave = np.sin(2 * np.pi * rate * t) / 2 + 0.5
    return data * dry + (data * modwave) * wet
