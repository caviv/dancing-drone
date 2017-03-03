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
		self.thrust_mult = 1
		self.thrust_step = 500
		self.thrust = 20000
		self.maxthrust = 50000
		self.pitch = 0
		self.roll = 0
		self.yaw = -127
		self.stopping = False

		Thread(target=self.gui).start()
		self.crazyflie = Crazyflie()
		cflib.crtp.init_drivers()
        # You may need to update this value if your Crazyradio uses a different frequency.
		self.crazyflie.open_link("radio://0/10/250K")
		#self.crazyflie.open_link("radio://0/6/1M")
		self.crazyflie.connectSetupFinished.add_callback(self.connectSetupFinished)
 
    def connectSetupFinished(self, linkURI):
        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        Thread(target=self.pulse_command).start()

    def gui(self):
		print "bingo"
		while True:
			#nb = _GetchUnix()
			nb = sys.stdin.read(1)
			if nb=='x':
				self.stopping = True
				sys.exit()
			if nb=='r':
				self.thrust = self.thrust + 2000
			if nb=='f':
				self.thrust = self.thrust - 2000
			if nb=='e':
				self.yaw = self.yaw + 0.2
			if nb=='q':
				self.yaw = self.yaw - 0.2
			if nb=='d':
				self.roll = self.roll + 0.2
			if nb=='a':
				self.roll = self.roll - 0.2
			if nb=='w':
				self.pitch = self.pitch - 0.2
			if nb=='s':
				self.pitch = self.pitch + 0.2
				
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
			self.crazyflie.commander.send_setpoint(self.roll, self.pitch, self.yaw, self.thrust)
			time.sleep(0.50)
			
			#if (thrust >= maxthrust):
			#	thrust_mult = -1
			#thrust = thrust + (thrust_step * thrust_mult)
		self.crazyflie.commander.send_setpoint(0,0,0,0)       
		time.sleep(0.1)
		self.crazyflie.close_link()


Main()
