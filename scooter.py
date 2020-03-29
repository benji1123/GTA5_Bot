import time
from vehicle import Vehicle


class Scooter(Vehicle):

	def __init__(self, accelerate=False, brake=False, angle=0):
		self.accelerate = accelerate
		self.brake = brake
		self.angle = angle
		print('scooter')