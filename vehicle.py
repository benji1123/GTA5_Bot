import time
from tools import keypresser as keybot


class Vehicle(object):
	def __init__(self):
		print('Vehicle')

	def brake(self):
		keybot.press('S')
		print('brake')

	def accelerate(self):
		keybot.press('W')
		print('accelerate')

	def steer(self, angle):
		print('steer @ {} deg'.format(angle))