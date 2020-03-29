from tools import keypresser as keybot
import numpy as np
import cv2
from PIL import ImageGrab
import time
import sys


class Bot(object):
    
    def __init__(self):
    	self.fov = None
    	print('bot created')

    '''
    Screen-Capture the Game Window
    '''
    def look(
    	self, preview=True, 
    	x1=0, y1=40, 
    	x2=800, y2=625):

    	# Screen Capture
        fov = np.array(ImageGrab.grab(bbox=(x1,y1,x2,y2)))
        self.fov = fov

        # Additional Processing
        processed_frame = process_img(fov)

        # Display
        if preview:
            cv2.imshow('screen', cv2.cvtColor(
    		    processed_frame, cv2.COLOR_BGR2RGB))

        
def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, 200, 300)
    return processed_img