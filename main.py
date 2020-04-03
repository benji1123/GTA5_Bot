from PIL import ImageGrab
import numpy as np
import cv2
import time
from time import sleep
from scooter_bot import ScooterBot
import pyautogui


def main():
    frame_count = 0
    start_time = time.time()
    bot = ScooterBot()

    '''
    Control Loop
    '''
    while True:
        bot.look(False)
        # img = bot.fov
        img = bot.show_lanelines()
        # print(img.shape)
        # cv2.imshow('', cv2.bitwise_and(bot.fov, self.roi))
        cv2.imshow('', img)


        frame_count += 1

        # QUIT
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            # Compute FPS
            print('\n\nFPS = {}'.format(
            	str(frame_count/(time.time()-start_time))))
            break


if __name__ == '__main__':
    main()