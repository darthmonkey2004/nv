import numpy as np
from mss import mss as sct
from imutils import resize
import cv2

class screengrab():
	def __init__(self, width=640, height=480):
		self.cap = sct()
		self.monitor = self.cap.monitors[1]
		self.width = width
		self.height = height

	def read(self):	
		ret = False
		try:
			img = resize(np.array(self.cap.grab(self.monitor)), width=self.width, height=self.height)
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
			ret = True
		except Exception as e:
			img = None
			print(f"Error - Couldn't get screenshot! ({e}")
			ret = False
		return ret, img

	def release(self):
		#pseudo function for cv2 read compatability.
		pass
		
