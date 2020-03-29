from bot import Bot
from scooter import Scooter
import numpy as np
import cv2


class ScooterBot(Bot):
    def __init__(self):
    	self.scooter = Scooter()