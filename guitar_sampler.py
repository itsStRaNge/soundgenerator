from scipy.io.wavfile import write
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np

MAX_FREQ = 22000
SAMPLE_RATE = 2 * MAX_FREQ + 100
VOLUME = 6000

def display():
    rate, guitar = read('guitar.wav')
    guitar = np.int16(guitar / np.max(np.abs(guitar)) * VOLUME)
    x = np.linspace(0, len(guitar), len(guitar))
    # g_yf = fft(guitar)
    g_yf = np.fft.fft(guitar)
    g_yf[(SAMPLE_RATE // 2) + 50:] = 0
    xf = np.linspace(0, len(g_yf), len(g_yf))
    re_guitar = np.fft.ifft(g_yf)

    f, axarr = plt.subplots(4)
    axarr[0].plot(x, guitar)
    axarr[0].set_title('Guitar (Signal)')
    axarr[0].grid()

    axarr[1].plot(xf[0:SAMPLE_RATE // 2], g_yf[0:SAMPLE_RATE // 2], color='g')
    axarr[1].set_title('Guitar FFT')
    axarr[1].grid()

    re_guitar = np.int16(re_guitar.real / np.max(np.abs(re_guitar.real)) * VOLUME)
    write('re_guitar.wav', SAMPLE_RATE, re_guitar)
    axarr[2].plot(xf, re_guitar)
    axarr[2].set_title('Guitar IFFT (Signal)')
    axarr[2].grid()

    axarr[3].plot(xf, (guitar - re_guitar), color='r')
    axarr[3].set_title('Error')
    axarr[3].grid()

    plt.show()


display()