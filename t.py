# Dancing Dron - CrazyFly dancing for music beat
# Cnaan Aviv 2013-10-05

import time, sys
import usb
from threading import Thread
import logging
import cflib
from cflib.crazyflie import Crazyflie
from cfclient.utils.logconfigreader import LogConfig
from cfclient.utils.logconfigreader import LogVariable

#import alsaaudio, time, audioop

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
#inp.setchannels(1)
#inp.setrate(8000)
#inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
#inp.setperiodsize(160)


logging.basicConfig(level=logging.INFO)

class Main:

    def __init__(self):
        #Thread(target=self.micmem).start()
        print "x"


    def a(self):
        print "a"

Main()
