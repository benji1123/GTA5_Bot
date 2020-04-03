from bot import Bot
from scooter import Scooter
import numpy as np
import cv2


class ScooterBot(Bot):
    def __init__(self):
    	self.scooter = Scooter()
    	self.roi = create_mask()

    def accelerate(self):
    	self.scooter.accelerate()

    def brake(self):
    	self.scooter.brake()

    
'''
Create Mask
for getting ROI 
'''
def create_mask():
	mask = np.zeros((800,800))
	vertices = np.array(
		[[10,500],  [10,300], 
		  [300,200],[500,200], 
		  [800,300],[800,500]]
	)
	print(vertices[0,0].dtype)
	return np.uint8(cv2.fillPoly(mask, [vertices], 255))
