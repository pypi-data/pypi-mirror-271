'''
Created on 15 Feb 2015

@author: Ronny Andersson (ronny@andersson.tk)
@copyright: (c) 2015 Ronny Andersson
@license: MIT
'''

# Standard library
import logging

# Internal
from zignal.audio import Audio, Noise, Sinetone

if __name__ == '__main__':
    logging.basicConfig(
        format="%(levelname)-8s: %(module)s.%(funcName)-15s %(message)s",
        level="DEBUG",
        )
    # some libraries are noisy in DEBUG
    logging.getLogger("matplotlib").setLevel(logging.INFO)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    fs  = 10000
    f0  = 10
    dur = 0.1

    x1  = Sinetone(f0=f0, fs=fs, duration=dur+0.2, gaindb=0)
    xn  = Noise(fs=fs, duration=dur, gaindb=-20)
    x   = Audio(fs=fs)

    print(x)

    x.append(xn, x1)
    del x1, xn

    print(x)

    x.plot(ch='all')
