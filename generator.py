import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import sounddevice as sd
import effect
import tone

VOLUME = 15000
MAX_FREQ = 22000  # in hz
TONE = 880  # in hz
SYNTETHIC_DIR = 'synthetics/'


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


if __name__ == '__main__':
    # TODO: use a chooser to select instrument
    instrument_list = tone.get_instruments()
    choosen_instrument = instrument_list[0]

    # generate tone
    signal, freq, envelope = tone.generate_note(TONE, choosen_instrument)

    # apply effects
    # signal = effect.flanger(signal)
    # signal = effect.tremolo(signal)

    # set volume
    scaled = np.int16(signal * VOLUME)  # apply volume

    # save and display result
    write(SYNTETHIC_DIR + choosen_instrument, 44100, scaled)
    sd.play(data=scaled, samplerate=44100)
    display(signal, freq, envelope, 44100)
