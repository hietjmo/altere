import numpy as np
from soundfile import SoundFile
import math
np.tau = math.tau

samplerate = 44100
rate = 44100
volume = 0.3

finlandia = """
Oi, Suomi, katso, sinun päiväs' koittaa,
yön uhka karkoitettu on jo pois,
ja aamun kiuru kirkkaudessa soittaa,
kuin itse taivahan kansi sois'.
Yön vallat aamun valkeus jo voittaa,
sun päiväs' koittaa, oi synnyinmaa.

Oi, nouse, Suomi, nosta korkealle,
pääs' seppelöimä suurten muistojen.
Oi, nouse, Suomi, näytit maailmalle,
sa että karkoitit orjuuden,
ja ettet taipunut sa sorron alle,
on aamus' alkanut, synnyinmaa.
""" # Veikko Antero Koskenniemi, 1940

average_male_vowel_formants = """ WIKIPEDIA
i 	240 	2400 	2160
y 	235 	2100 	1865
e 	390 	2300 	1910
ø 	370 	1900 	1530
ɛ 	610 	1900 	1290
œ 	585 	1710 	1125
a 	850 	1610 	760
ɶ 	820 	1530 	710     (?)
ɑ 	750 	940 	190
ɒ 	700 	760 	60
ʌ 	600 	1170 	570
ɔ 	500 	700 	200
ɤ 	460 	1310 	850
o 	360 	640 	280
ɯ 	300 	1390 	1090
u 	250 	595 	345 

formants = {
  "i":240, "y":235, "e":390, "ö":370, "ä":820, "a":750, "u":250, "o":360,
  " ": 0,
}
"""

formants = {
  " ": 0,
  "i": 321,
  "e": 443,
  "ä": 600,
  "y": 330,
  "ö": 436,
  "a": 609,
  "o": 433,
  "u": 332,
} # Iivonen, p. 31

print (formants)

finlandia = finlandia.replace ("\n","  ")
vows = [formants[c] for c in finlandia.lower() if c in formants]

print ("vows =",vows)

fs = 44100  # sampling rate, Hz, must be integer
duration = 0.25  # in seconds, may be float

with SoundFile('audio.wav', 'w', 44100, 1, 'PCM_24') as tf:
  for f in vows:
    sample = (volume * np.sin (np.tau * np.arange(fs * duration) * f / fs)).astype(np.float32) 
    tf.write(sample)

# Iivonen, Antti: Kielten vokaalit kuuloanalogisessa vokaalikartassa. Puhe ja kieli, 21:1, 17−43 (2012).

