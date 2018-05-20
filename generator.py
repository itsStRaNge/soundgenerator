import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt


VOLUME = 15000
AUDIO_LEN = 1  # in sec
MAX_FREQ = 22000  # in hz
SAMPLE_FREQ = MAX_FREQ  # * 2 + 100  # in hz
SAMPLES = SAMPLE_FREQ * AUDIO_LEN  # N
TONE = 440  # in hz

# range of influence of overtone, if near 0 then only overtone is used
F_WEIGHTS_GAUSSIAN_SIGMA = 5


def gaussian(x, mu):
    return np.exp(-np.square(x - float(mu)) / np.power(F_WEIGHTS_GAUSSIAN_SIGMA, 2.))


def fade_out(time, freq):
    m = np.log(0.2) / (TONE- MAX_FREQ)
    alpha = np.exp((freq - MAX_FREQ) * m)  # alpha(f_root)= 0.2 and alpha(f_max)= 1
    fade = np.exp(- time * alpha * 1.6)
    return fade


def generate_note(f_root):
    # init vars
    num_overtones = 5  # int(MAX_FREQ / TONE) - 1

    # init arrays
    f_spec = np.linspace(f_root, MAX_FREQ, MAX_FREQ - f_root)  # array with freq from main tone to max freq
    signal_fft = np.zeros(f_spec.shape)

    # fill weights of overtones
    for i in range(0, num_overtones):
        signal_fft += gaussian(f_spec, f_spec[i*f_root]) * np.exp(-i * 0.05) * 100

    # generate tone
    tone = np.fft.ifft(signal_fft)
    tone = np.int16( tone/np.max(np.abs(tone)) * VOLUME)  # normalize and scale for volume
    return tone, signal_fft


def display(signal, signal_fft):
    f, axarr = plt.subplots(5)
    t = AUDIO_LEN / SAMPLES

    # create x aches for time, weights and fourier
    xf = np.linspace(0.0, 1.0 / (2.0 * t), MAX_FREQ // 2)
    xw = np.linspace(TONE, MAX_FREQ, MAX_FREQ - TONE)
    xt = np.linspace(0, AUDIO_LEN, SAMPLES)

    # plot everything
    axarr[0].plot(xt, signal)
    axarr[0].set_title('Ton')
    axarr[0].grid()

    axarr[1].plot(xf, 2.0/MAX_FREQ * np.abs(signal_fft[0:MAX_FREQ//2]))
    axarr[1].set_title('FFT')
    axarr[1].grid()

    axarr[2].plot(xw, signal_fft)
    axarr[2].set_title('Weights')
    axarr[2].grid()
    plt.show()

signal, frequencies = generate_note(TONE)
write('samples/generated.wav', SAMPLES, signal)
display(signal, frequencies)
