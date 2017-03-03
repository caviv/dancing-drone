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

logging.basicConfig(level=logging.INFO)

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class Main:

    def __init__(self):
		self.thrust = 25000
		self.pitch = -4
		self.roll = 1
		self.yaw = 0

		self.stopping = False
		self.jump = 0
		self.backward = 0
		self.forward = 0

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

    def gui(self):
		print "bingo"
		while self.stopping==False:
			#nb = _GetchUnix()
			nb = sys.stdin.read(1)
			if nb=='x':
				self.stopping = True
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
				self.thrust = 39000

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
				lthrust = self.thrust + 25000
			if self.forward > 0:
				lpitch = self.pitch + 4
			if self.backward > 0:
				lpitch = self.pitch - 4
			self.crazyflie.commander.send_setpoint(self.roll, lpitch, self.yaw, lthrust)
			time.sleep(0.15)
			self.jump = self.jump - 1;
			self.forward = self.forward - 1;
			self.backward = self.backward - 1;
			
		self.crazyflie.commander.send_setpoint(0,0,0,0)       
		time.sleep(0.1)
		self.crazyflie.close_link()


Main()
