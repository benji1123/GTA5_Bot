from tools import keypresser as keybot
import numpy as np
import cv2
from PIL import ImageGrab
import time
import sys

from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean


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
                    0,0,800,800)), 
                dtype=np.uint8)
        except OSError:
            print('OSError: cannot capture screen')


    '''
    Image Processing
    https://towardsdatascience.com/finding-lane-lines-simple-pipeline-for-lane-detection-d02b62e7572b
    '''
    def show_lanelines(self):
        img = cv2.cvtColor(self.fov, cv2.COLOR_BGR2GRAY) # monochrome
        img = cv2.Canny(self.fov, 200, 300)                      # get edges only
        img = cv2.GaussianBlur(img, (5,5), 0)          # mitigate aliasing
        img = cv2.bitwise_and(img, self.roi)                # remove non-ROI
        
        # get lines as coordinate-pairs from frame 
        lines = cv2.HoughLinesP(img, 1, np.pi/180,          
                                180, np.array([]),
                                100,5)     
        # default slope-values       
        m1 = 0
        m2 = 0
        try:
            l1, l2, m1,m2 = draw_lanes(self.fov, lines)
            cv2.line(self.fov, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 7)
            cv2.line(self.fov, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 7)
        except Exception as e:
            print(str(e))
            pass

        return self.fov


'''
Derive two lanes
from raw line-detector data
'''
def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):
    try:
        ys = []  
        for i in lines:
            for ii in i:
                ys += [ii[1],ii[3]]
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        for idx,i in enumerate(lines):
            for xyxy in i:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                x_coords = (xyxy[0],xyxy[2])
                y_coords = (xyxy[1],xyxy[3])
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m
                line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])
        
        final_lanes = {}
        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]
            
            if len(final_lanes) == 0:
                final_lanes[m] = [ [m,b,line] ]
            else:
                found_copy = False
                for other_ms in final_lanes_copy:
                    if not found_copy:
                        if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                            if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                                final_lanes[other_ms].append([m,b,line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [ [m,b,line] ]
        line_counter = {}
        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])
        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]
        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])
        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id

    except Exception as e:
        print(str(e))