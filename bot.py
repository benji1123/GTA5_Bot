from tools import keypresser as keybot
import numpy as np
import cv2
from PIL import ImageGrab
import time
import sys


class Bot(object):
    
    def __init__(self):
        self.fov = None
        self.roi = None # mask for isolating ROI in image-frame
        print('bot created')

    '''
    Screen-Capture the Game Window
    '''
    def look(self, preview=True):
        try:
            # single-channel greyscale image
            self.fov = np.asarray(
                ImageGrab.grab(bbox=(
                    0,0,800,800)).convert('L'), 
                dtype=np.uint8)

        except OSError:
            print('OSError: cannot capture screen')

    '''
    Image Processing
    '''
    def show_lanelines(self):
        img = cv2.Canny(self.fov, 200, 300)                 # get edges only
        img = cv2.GaussianBlur(img, (3,3), 0)               # mitigate aliasing
        img = cv2.bitwise_and(img, self.roi)                # remove non-ROI
        # get lines as coordinate-pairs from frame 
        lines = cv2.HoughLinesP(img, 1, np.pi/180,          
                                180, np.array([]),
                                100,5)             

        try:
            # draw detected lines
            for l in lines:
                cv2.line(img, 
                         (l[0,0],l[0,1]), 
                         (l[0,2],l[0,3]), 
                         [255,255,255],
                         3)

        except TypeError:
            print('No lines detected')
            pass

        return img