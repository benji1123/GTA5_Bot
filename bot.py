from tools import keypresser as keybot
import numpy as np
import cv2
from PIL import ImageGrab
import time
import sys


class Bot(object):
    
    def __init__(self):
        self.fov = None
        self.roi = None
        print('bot created')

    '''
    Screen-Capture the Game Window
    '''
    def look(self, preview=True):
        # Screen Capture
        self.fov = np.asarray(ImageGrab.grab(bbox=(0,0,800,800)).convert('L'), 
            dtype=np.uint8)
        print(self.fov.shape)

    def canny(self, img):
        processed_img = cv2.Canny(img, threshold1=200, threshold2=300)
        return processed_img

    def isolate_roi(self, img, mask):
        return cv2.bitwise_and(img, mask)

    def show_lanelines(self):
        img = self.canny(self.fov)
        img = cv2.GaussianBlur(img, (5,5), 0)
        img = self.isolate_roi(img, self.roi)  
        lines = cv2.HoughLinesP(img, 1, np.pi/180, 180, 20, 15)

        try:
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(img, (x1,y1), (x2,y2), [255,255,255], 3)
        except:
            pass # sorry (in-case there are no lines)

        return img