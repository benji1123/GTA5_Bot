from PIL import ImageGrab
import numpy as np
import cv2
import time

def main():
	start_time = time.time()
	frame_count = 0
	while True:
		# GTA-V window set @ top-left corner of screen
		frame = np.array(ImageGrab.grab(bbox=(0,40,800,625)))
		cv2.imshow('screen', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

		frame_count += 1
		if cv2.waitKey(25) & 0xFF == ord('q'):
	            cv2.destroyAllWindows()
	            print('\n\nFPS = {}'.format(str(frame_count/(time.time()-start_time))))
	            break

if __name__ == '__main__':
	main()