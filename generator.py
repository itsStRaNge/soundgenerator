import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from scipy.fftpack import ifft
from scipy.signal import hilbert
import matplotlib.pyplot as plt
import sounddevice as sd
import effect


VOLUME = 15000
MAX_FREQ = 22000  # in hz
SAMPLE_FREQ = MAX_FREQ  #* 2 + 100  # in hz
TONE = 440  # in hz


def get_hilbert(file):
    analytic_signal = hilbert(file)
    return np.abs(analytic_signal)


def generate_note(f_root, overtones=4):
    # get envelope
    fs, envelope_signal = read('guitar.wav')
    envelope = get_hilbert(envelope_signal)

    # calculate spectrum
    f_spec = np.zeros(MAX_FREQ)
    for i in range(0, overtones):
        try:
            f_spec[i*f_root + f_root] = 1 / (i * i + 1)
        except IndexError:
            break

    # get signal from spectrum
    note = ifft(f_spec, len(envelope_signal))

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
scaled = np.int16(data.real/np.max(np.abs(data.real)) * VOLUME)  # normalize

affected = effect.flanger(scaled)
write('test.wav', fs, scaled)
sd.play(data=affected, samplerate=fs)
display(affected, freq, envelope, fs)
