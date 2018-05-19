import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from scipy.fftpack import fft
from scipy.fftpack import ifft
import matplotlib.pyplot as plt


VOLUME = 15000
AUDIO_LEN = 1  # in sec
MAX_FREQ = 22000  # in hz
SAMPLE_FREQ = MAX_FREQ #* 2 + 100  # in hz
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
    time_line = np.linspace(0, AUDIO_LEN, SAMPLES)
    f_spec = np.linspace(f_root, MAX_FREQ, MAX_FREQ - f_root)  # array with freq from main tone to max freq
    f_prop = np.zeros(f_spec.shape)
    note = np.zeros(time_line.shape)

    # fill weights of overtones
    for i in range(0, num_overtones):
        gaus = gaussian(f_spec, f_spec[i*f_root]) * np.exp(-i*0.05) * 100
        f_prop += gaus
        # f_prop[i*f_root] = 1

    # generate tone
    a = np.pi * time_line  # outside for-loop for performance
    for i in range(0, len(f_spec)):
        if f_prop[i] != 0.0:
            note += np.sin(f_spec[i] * a) * float(f_prop[i]) * fade_out(time_line, f_spec[i])
    return note, f_prop


def display(tone, weights):
    t = AUDIO_LEN / SAMPLES
    xf = np.linspace(0.0, 1.0 / (2.0 * t), MAX_FREQ // 2)
    yf = fft(tone)

    xw = np.linspace(TONE, MAX_FREQ, MAX_FREQ - TONE)
    xt = np.linspace(0, AUDIO_LEN, SAMPLES)

    f, axarr = plt.subplots(5)
    axarr[0].plot(xt, tone)
    axarr[0].set_title('Ton')
    axarr[0].grid()
    axarr[1].plot(xf, 2.0/MAX_FREQ * np.abs(yf[0:MAX_FREQ//2]))
    axarr[1].set_title('FFT')
    axarr[1].grid()
    axarr[2].plot(xw, weights)
    axarr[2].set_title('Weights')
    axarr[2].grid()

    rate, guitar = read('guitar.wav')
    g_yf = fft(guitar)
    axarr[3].plot(xf, 2.0/MAX_FREQ * np.abs(g_yf[0:MAX_FREQ//2]))
    axarr[3].set_title('Guitar')
    axarr[3].grid()
    plt.show()

data, weight = generate_note(TONE)
scaled = np.int16( data/np.max(np.abs(data)) * VOLUME)  # normalize and scale for volume
write('test.wav', SAMPLES, scaled)
display(scaled, weight)
