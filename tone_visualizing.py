from scipy.io.wavfile import write
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np

MAX_FREQ = 22000
SAMPLE_RATE = 2 * MAX_FREQ + 100
VOLUME = 6000

def display(file):
    rate, signal_y = read('samples/' + file)
    f, axarr = plt.subplots(4)

    """ NORMAL SIGNAL """
    # normalize signal
    signal_y = np.int16(signal_y / np.max(np.abs(signal_y)) * VOLUME)
    signal_x = np.linspace(0, len(signal_y), len(signal_y))

    # plot
    axarr[0].plot(signal_x, signal_y)
    axarr[0].set_title('Signal')
    axarr[0].grid()

    """ FFT SIGNAL """
    # create fft of signal and low pass filter it
    signal_fft_y = np.fft.fft(signal_y)
    fft_x = np.linspace(0, len(signal_fft_y), len(signal_fft_y))
    signal_fft_y[(SAMPLE_RATE // 2) + 50:] = 0

    # plot
    axarr[1].plot(fft_x[0:SAMPLE_RATE // 2], signal_fft_y[0:SAMPLE_RATE // 2], color='g')
    axarr[1].set_title('FFT')
    axarr[1].grid()

    """ IFFT SIGNAL """
    # create ifft signal and normalize
    signal_ifft_y = np.fft.ifft(signal_fft_y)
    signal_ifft_y = np.int16(signal_ifft_y.real / np.max(np.abs(signal_ifft_y.real)) * VOLUME)

    # plot and save ifft signal
    write('samples/ifft_' + file, SAMPLE_RATE, signal_ifft_y)
    axarr[2].plot(signal_x, signal_ifft_y)
    axarr[2].set_title('IFFT')
    axarr[2].grid()

    # plot error of signal and ifft signal
    axarr[3].plot(signal_x, (signal_y - signal_ifft_y), color='r')
    axarr[3].set_title('Error')
    axarr[3].grid()

    plt.show()


display('guitar.wav')
