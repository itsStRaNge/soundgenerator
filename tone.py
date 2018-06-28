import numpy as np
from scipy.io.wavfile import read
from scipy.fftpack import ifft
from scipy.signal import hilbert
import os

SAMPLE_DIR = 'samples/'
AUDIO_FORMAT = '.wav'


def get_instruments():
    instruments = []
    for file in os.listdir(SAMPLE_DIR):
        if file.endswith(AUDIO_FORMAT):
            instruments.append(file.title())
    return instruments


def generate_note(f_root, instrument, overtones=4, fs=22000):
    """
    :param f_root: root frequency of the note in Hz
    :param instrument: instrument that gets imitate, call get_instruments() to check available ones
    :param overtones: number of overtones used
    :param fs: max number of frequencies used to generate tone
    :return: tone as signal, as spectrum, as envelope
    """
    # get envelope
    envelope = _get_envelope(instrument)

    # calculate spectrum
    f_spec = _get_spectrum(f_root, overtones, fs)

    # get signal from spectrum
    note = ifft(f_spec, len(envelope))

    # apply envelope for transient response and normalize
    note = note * envelope
    note = note.real / np.max(np.abs(note.real))
    return note, f_spec, envelope


def _get_envelope(file):
    fs_sample, envelope_signal = read(SAMPLE_DIR + file)
    return _get_hilbert_envelope(envelope_signal)


def _get_hilbert_envelope(signal):
    analytic_signal = hilbert(signal)
    return np.abs(analytic_signal)


def _get_spectrum(root, overtones, fs):
    f_spec = np.zeros(fs)
    for i in range(0, overtones):
        try:
            f_spec[i*root + root] = 1 / (i ** 3 + 1)
        except IndexError:
            break
    return f_spec
