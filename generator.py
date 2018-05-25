import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from scipy.fftpack import fft
from scipy.signal import hilbert
import matplotlib.pyplot as plt


VOLUME = 15000
MAX_FREQ = 22000  # in hz
SAMPLE_FREQ = MAX_FREQ  #* 2 + 100  # in hz
TONE = 440  # in hz


def get_hilbert(file):
    analytic_signal = hilbert(file)
    return np.abs(analytic_signal)


def generate_note(f_root):
    # init vars
    num_overtones = 5  # int(MAX_FREQ / TONE) - 1
    fs, envelope_signal = read('guitar.wav')

    # init arrays
    envelope = get_hilbert(envelope_signal)
    time_line = np.linspace(0.0, len(envelope_signal) / fs, len(envelope_signal))
    f_spec = np.linspace(0, MAX_FREQ, MAX_FREQ)  # array with freq from main tone to max freq
    note = np.zeros(time_line.shape)

    a = np.pi * time_line * f_root  # outside for-loop for performance
    # fill weights of overtones
    for i in range(0, num_overtones):
        f_spec[i*f_root + f_root] = 1
        note += np.sin(i * a)

    # apply envelope for transient response
    note = note * envelope
    return note, f_spec, envelope, fs


def display(tone, freq, envelope, fs):
    xf = np.linspace(0, len(freq), len(freq))

    xt = np.linspace(0, len(tone) / fs, len(tone))

    f, axarr = plt.subplots(3)
    axarr[0].plot(xt, tone)
    axarr[0].set_title('Ton')
    axarr[0].grid()

    axarr[1].plot(xf, freq)
    axarr[1].set_title('FFT')
    axarr[1].grid()

    axarr[2].plot(xt, envelope)
    axarr[2].set_title('Envelope')
    axarr[2].grid()
    plt.show()

data, freq, envelope, fs = generate_note(TONE)
scaled = np.int16( data/np.max(np.abs(data)) * VOLUME)  # normalize and scale for volume
write('test.wav', fs, scaled)
display(scaled, freq, envelope, fs)
