from PIL import ImageGrab
import numpy as np
import cv2
import time
from scooter_bot import ScooterBot


def main():
    frame_count = 0
    start_time = time.time()
    bot = ScooterBot()

    '''
    Control Loop
    '''
    while True:
        bot.look()
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