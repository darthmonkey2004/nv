
class detection():
	def __init__(self, img, rect=None, label='Unlabeled Detection', confidence=0.0):
		self.CONFIDENCE = confidence
		self.NAME = label
		self.IMAGE = img
		self.RECT = rect
		if self.RECT is not None:
			self.LEFT, self.TOP, self.RIGHT, self.BOTTOM = self.RECT
			#print(self.LEFT, self.TOP, self.RIGHT, self.BOTTOM)
			self.HEIGHT = self.BOTTOM - self.TOP
			self.WIDTH = self.RIGHT - self.LEFT
			self.CENTER_X = (self.WIDTH / 2) + self.LEFT
			self.CENTER_Y = (self.HEIGHT / 2) + self.TOP
			self.CENTER = self.CENTER_X, self.CENTER_Y
		else:
			self.LEFT, self.TOP, self.RIGHT, self.BOTTOM, self.CENTER_X, self.CENTER_Y, self.CENTER, self.WIDTH, self.HEIGHT = None, None, None, None, None, None, None, None, None

