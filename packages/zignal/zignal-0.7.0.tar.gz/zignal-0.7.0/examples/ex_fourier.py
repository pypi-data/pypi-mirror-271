'''
Created on 16 Feb 2015

@author: Ronny Andersson (ronny@andersson.tk)
@copyright: (c) 2015 Ronny Andersson
@license: MIT
'''

# Standard library
import logging

# Internal
from zignal.audio import Audio, FourierSeries

if __name__ == '__main__':
    logging.basicConfig(
        format="%(levelname)-8s: %(module)s.%(funcName)-15s %(message)s",
        level="DEBUG",
        )
    # some libraries are noisy in DEBUG
    logging.getLogger("matplotlib").setLevel(logging.INFO)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    dur = 0.1
    f0  = 20

    k   = Audio()
    x0  = FourierSeries(f0=f0, duration=dur, harmonics=0,  gaindb=-15)  # fundamental + 0 harmonics
    x1  = FourierSeries(f0=f0, duration=dur, harmonics=1,  gaindb=-15)  # fundamental + 1 harmonics
    x2  = FourierSeries(f0=f0, duration=dur, harmonics=2,  gaindb=-9)   # fundamental + 2 harmonics
    x3  = FourierSeries(f0=f0, duration=dur, harmonics=3,  gaindb=-9)   # ...
    x4  = FourierSeries(f0=f0, duration=dur, harmonics=4,  gaindb=-3)
    x5  = FourierSeries(f0=f0, duration=dur, harmonics=5,  gaindb=-3)
    x60 = FourierSeries(f0=f0, duration=dur, harmonics=60, gaindb=0)    # fundamental + 60 harmonics

    k.append(x0, x1, x2, x3, x4, x5, x60)
    print(k)
    k.plot(ch='all')
