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

import alsaaudio, time, audioop

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)


logging.basicConfig(level=logging.INFO)

class Main:

	def __init__(self):
		self.listen = True
		
		self.thrust = 25000
		self.pitch = -4
		self.roll = 0
		self.yaw = 0

		self.stopping = False
		self.jump = 0
		self.backward = 0
		self.forward = 0

		Thread(target=self.micmem).start()
		Thread(target=self.gui).start()
		self.crazyflie = Crazyflie()
		cflib.crtp.init_drivers()
		# You may need to update this value if your Crazyradio uses a different frequency.
		#self.crazyflie.open_link("radio://0/7/250K")
		self.crazyflie.open_link("radio://0/10/250K")
		#self.crazyflie.open_link("radio://0/6/1M")
		self.crazyflie.connectSetupFinished.add_callback(self.connectSetupFinished)

	def connectSetupFinished(self, linkURI):
		# Start a separate thread to do the motor test.
		# Do not hijack the calling thread!
		Thread(target=self.pulse_command).start()

	def micmem(self):
		while self.listen:
			# Read data from device
			l,data = inp.read()
			last = 0
			if l:
				# Return the maximum of the absolute value of all samples in a fragment.
				au = audioop.max(data, 2)
				print au
				if au >= 32676 and last <> 32676:
					print au
					self.jump = 1
				last = au
			time.sleep(.001)

	def gui(self):
		print "bingo"
		while self.stopping==False:
			#nb = _GetchUnix()
			nb = sys.stdin.read(1);
			if nb=='x':
				self.stopping = True
				self.listen = False
			if nb=='r':
				self.thrust = self.thrust + 1000
			if nb=='f':
				self.thrust = self.thrust - 1000

			if nb=='y':
				self.backward = 0
				self.forward = 3
			if nb=='h':
				self.backward = 3
				self.forward = 0

			if nb=='3':
				self.thrust = 35000
			if nb=='4':
				self.thrust = 40000

			if nb=='e':
				self.yaw = self.yaw + 1
			if nb=='q':
				self.yaw = self.yaw - 1
			if nb=='d':
				self.roll = self.roll + 2
			if nb=='a':
				self.roll = self.roll - 2
			if nb=='w':
				self.pitch = self.pitch - 2
			if nb=='s':
				self.pitch = self.pitch + 2

			if nb=='z':
				self.jump = 2
				
			sys.stdout.write("thrust=")
			print self.thrust
			sys.stdout.write("yaw=")
			print self.yaw
			sys.stdout.write("pitch=")
			print self.pitch
			sys.stdout.write("roll=")
			print self.roll

	def pulse_command(self):
		while self.stopping == False:
			lthrust = self.thrust
			lpitch = self.pitch
			if self.jump > 0:
				lthrust = self.thrust + 20000
				self.jump = self.jump - 1;
			if self.forward > 0:
				lpitch = self.pitch + 4
				self.forward = self.forward - 1;
			if self.backward > 0:
				lpitch = self.pitch - 4
				self.backward = self.backward - 1;
			self.crazyflie.commander.send_setpoint(self.roll, lpitch, self.yaw, lthrust)
			time.sleep(0.15)
			
		self.crazyflie.commander.send_setpoint(0,0,0,0)	   
		time.sleep(0.1)
		self.crazyflie.close_link()


Main()
