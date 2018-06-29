import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
from scipy.fftpack import fft
from scipy.fftpack import ifft


def show(tone, freq, envelope, fs):
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


def phase_correlation(l, r):
    # https://dsp.stackexchange.com/questions/1671/calculate-phase-angle-between-two-signals-i-e-digital-phase-meter
    # i think this feature is only useful in real time signal processing
    phase = np.arctan(np.divide(l, r))
    phase = np.nan_to_num(phase)

    magnitude = np.sqrt((np.power(l, 2) + np.power(r, 2)))
    magnitude = np.nan_to_num(magnitude)

    correlation = phase * magnitude
    correlation = correlation / np.max(np.abs(correlation))
    plt.plot(correlation)
    plt.show()

if __name__ == '__main__':
    fs, a = read('samples/guitar.wav')
    fs, b = read('synthetics/Guitar.Wav')
    phase_correlation(a, b)
