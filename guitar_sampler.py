from scipy.io.wavfile import write
from scipy.io.wavfile import read
from scipy.fftpack import fft
from scipy.fftpack import ifft
import matplotlib.pyplot as plt
import numpy as np

MAX_FREQ = 22000
SAMPLE_RATE = 2 * MAX_FREQ

def display():
    rate, guitar = read('guitar.wav')
    x = np.linspace(0, len(guitar), len(guitar))
    # g_yf = fft(guitar)
    g_yf = np.fft.fft(guitar)
    xf = np.linspace(0, len(g_yf), len(g_yf))
    re_guitar = np.fft.ifft(g_yf)

    print("gutiar %s" % guitar.shape)
    print("g_f %s" % g_yf.shape)
    print("re guitar %s" % re_guitar.shape)
    write('re_guitar.wav', rate, re_guitar.imag)

    f, axarr = plt.subplots(3)
    axarr[0].plot(x, guitar)
    axarr[0].set_title('Guitar')
    axarr[0].grid()

    axarr[1].plot(xf[0:SAMPLE_RATE // 2], g_yf[0:SAMPLE_RATE // 2])
    axarr[1].set_title('Guitar FFT')
    axarr[1].grid()

    axarr[2].plot(xf, re_guitar)
    axarr[2].set_title('Guitar Inverse FFT')
    axarr[2].grid()
    plt.show()



display()