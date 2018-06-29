import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import effect
import tone
import plot

VOLUME = 15000
MAX_FREQ = 22000  # in hz
TONE = 880  # in hz
SYNTHETIC_DIR = 'synthetics/'


# TODO: use a chooser to select instrument
instrument_list = tone.get_instruments()
chosen_instrument = instrument_list[0]

# generate tone
signal, freq, envelope = tone.generate(TONE, chosen_instrument)

# apply effects
# signal = effect.flanger(signal)
# signal = effect.tremolo(signal)
# signal = effect.distortion(signal)
# signal = effect.reverb(signal)
signal = effect.chorus(signal, wet=0.5, delay=15)

# set volume
scaled = np.int16(signal * VOLUME)  # apply volume

# save and display result
write(SYNTHETIC_DIR + chosen_instrument, 44100, scaled)
sd.play(data=scaled, samplerate=44100)
plot.show(signal, freq, envelope, 44100)
