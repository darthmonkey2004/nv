import os
from opts import get_default_options
import platform
import threading
import cv2
from logger import logger
from conf import config
from detector import detector
from random import randint
from screengrab import *


log = logger().log
readConf = config().read
writeConf = config().write

class camera():
	def __init__(self, src=None, camera_id=None, start=True, show=False, process='object_detect', negative=False, contrast=1, brightness=1):
		self.CONTRAST = contrast
		self.BRIGHTNESS = brightness
		self.NEGATIVE = negative
		self.GRAY = False
		self.CONF = readConf()
		self.SHOW = show
		self.IS_RUNNING = False
		if src is not None:
			self.SRC = src
			if camera_id is not None:
				self.CAMERA_ID = camera_id
				#todo put in conflicting source (override) function
			else:
				self.CAMERA_ID = self.get_id_fromSrc(self.SRC)
		else:
			if camera_id is not None:
				self.CAMERA_ID = camera_id
				self.SRC = self.get_src_fromId(self.CAMERA_ID)
			else:
				raise Exception(f"Need either source or camera id!")
		try:
			self.CAP_TYPE = self.CONF['CAMERAS'][self.CAMERA_ID]['TYPE']
		except:
			self.CAP_TYPE = self.get_type(src=self.SRC)
		if self.CAP_TYPE == 'rpi':
				from picam import rpi
		if self.CAP_TYPE == 'screengrab':
			start = False
		self.CAP = self.get_capture(self.CAP_TYPE)
		ret, self.IMAGE = self.CAP.read()
		self.release = self.CAP.release
		self.CAMERA_NAME = f"Camera_{self.CAMERA_ID}"
		self.PROCESS = process
		if self.PROCESS:
			self.DETECTOR = detector()
		else:
			self.DETECTOR = None
		if start:
			self.start()
		self.THUMBNAIL = os.path.join(os.path.expanduser("~"), '.nv', f"Camera_{self.CAMERA_ID}.png")

	def writeThumbnail(self, img=None):
		if img is None:
			img = self.IMAGE
		if type(img) == tuple:
			ret, img = img
		cv2.imwrite(self.THUMBNAIL, img)

	def rdmTkColor(self):
		colors = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace', 'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff', 'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender', 'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray', 'light slate gray', 'gray', 'light gray', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue', 'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue', 'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue', 'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise', 'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green', 'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green', 'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green', 'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow', 'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown', 'sandy brown', 'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange', 'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink', 'pale violet red', 'maroon', 'medium violet red', 'violet red', 'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple', 'thistle', 'snow2', 'snow3', 'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'Slategray1', 'Slategray2', 'Slategray3', 'Slategray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3', 'cyan4', 'DarkSlategray1', 'DarkSlategray2', 'DarkSlategray3', 'DarkSlategray4', 'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4', 'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1', 'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2', 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2', 'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1', 'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'grey1', 'grey2', 'grey3', 'grey4', 'grey5', 'grey6', 'grey7', 'grey8', 'grey9', 'grey10', 'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19', 'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28', 'grey29', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37', 'grey38', 'grey39', 'grey40', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47', 'grey48', 'grey49', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56', 'grey57', 'grey58', 'grey59', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65', 'grey66', 'grey67', 'grey68', 'grey69', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74', 'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey80', 'grey81', 'grey82', 'grey83', 'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey90', 'grey91', 'grey92', 'grey93', 'grey94', 'grey95', 'grey97', 'grey98', 'grey99']
		return colors[randint(0, len(colors) - 1)]


	def adjust(self, img=None, brightness=None, contrast=None, negative=None, gray=None):
		if gray is None:
			gray = self.GRAY
		if brightness is not None:
			self.BRIGHTNESS = brightness
		if contrast is not None:
			self.CONTRAST = contrast
		if img is None:
			img = self.IMAGE
		if negative is not None:
			self.NEGATIVE = negative
		if self.NEGATIVE:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			img = abs(255-img)
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		if self.GRAY:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		else:
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		self.IMAGE = cv2.addWeighted(img, self.CONTRAST, img, 0, self.BRIGHTNESS)
		return self.IMAGE

	def set_default_opts(self):
		opts = get_default_options()
		for k, v in zip(list(opts.keys()), list(opts.values())):
			self.__dict__[k] = v
		self.CONF['OPTIONS'] = opts
		writeConf(self.CONF)

	def get_platform(self):
		dat = platform.uname()
		if 'rpi' in dat.release:
			return 'rpi'
		elif 'Ubuntu' in dat.version:
			return 'Ubuntu'

	def get_type(self, src=None):
		if src is None:
			src = self.SRC
		if 'x11://' in src:
			return 'screengrab'
		elif 'rtsp://' in src or 'http://' in src:
			return 'cv2'
		elif 'rpi://' in src or self.get_platform() == 'rpi':
			return 'rpi'

	def _next_id(self):
		ids = list(self.CONF['CAMERAS'].keys())
		return int(ids[len(ids) - 1]) + 1

	def get_src_fromId(self, camera_id=None):
		if camera_id is None:
			camera_id = self._next_id()
		try:
			return self.CONF['CAMERAS'][camera_id]['SRC']
		except Exception as e:
			log(f"ERROR - camera.py.get_src_fromID:{e}")
			return None

	def get_id_fromSrc(self, src):
		srcs = [self.CONF['CAMERAS'][camera_id]['SRC'] for camera_id in self.CONF['CAMERAS']]
		if src in srcs:
			idx = srcs.index(src)
			camera_id = list(self.CONF['CAMERAS'].keys())[idx]
			return camera_id
		else:
			return None

	def get_capture(self, capture_type=None):
		""" returns capture based on type.
		TODO - imagezmq, picam, screengrab"""
		print(f"Capture type: {capture_type}")
		if capture_type is None:
			capture_type = self.CAP_TYPE
		if capture_type == 'cv2':
			try:
				#return opencv video capture object
				return cv2.VideoCapture(self.SRC)
			except Exception as e:
				log(f"Error camera.py.get_capture:{e}")
				return None
		elif capture_type == 'screengrab':
			#return screengrab object
			return screengrab()
		elif capture_type == 'zmq':
			log(f"TODO - 'imagezmq' method")
			return None
		elif capture_type == 'rpi':
			return rpi(show=self.SHOW)


	def read(self):
		"""Read wrapper for cv2 cap.read function. for integration of other capture methods into wrapper class"""
		ret, self.IMAGE = self.CAP.read()
		if not ret:
			print("Error = Failed to get image!")
		return self.IMAGE
			

	def start(self):
		self.thread = threading.Thread(target=self.loop)
		self.thread.setDaemon(True)
		self.thread.start()
		log("camera.py.start:Thread started!")

	def loop(self):
		"""main loop. Executed in start method."""

		if self.SHOW:# if display image flag set...
			cv2.namedWindow(self.CAMERA_NAME, cv2.WINDOW_NORMAL)
			self.WINDOW = self.CAMERA_NAME
			ret, img = self.read()
			if ret:
				self.IMAGE_HEIGHT, self.IMAGE_WIDTH, c = img.shape
				#cv2.resizeWindow(self.CAMERA_NAME, (self.IMAGE_HEIGHT, self.IMAGE_WIDTH))
		else:
			self.WINDOW = None
		self.IS_RUNNING = True
		self.SKIP_FRAMES = 10
		self.FRAME_CT = 0
		while self.IS_RUNNING:
			self.FRAME_CT += 1
			#set run flag to img get result. if False, kills loop
			img = self.read()
			if type(img) == tuple:
				self.IS_RUNNING, img = img
			#self.IS_RUNNING, img = self.read()
			if self.IS_RUNNING:
					self.img = self.adjust(img=img)
			if not self.IS_RUNNING:
				log(f"camera.loop:Exiting (IS_RUNNING=False)")
				break
			if self.PROCESS is not None and self.DETECTOR is not None and self.FRAME_CT == self.SKIP_FRAMES:
				self.FRAME_CT = 0
				dets = self.DETECTOR.detect(self.IMAGE, self.PROCESS)
				if dets is not None:
					if dets != [] or len(dets) > 0:
						self.IMAGE = self.draw_on_image(img=self.IMAGE, dets=dets)
			if self.SHOW:
				if self.WINDOW is None:
					cv2.namedWindow(self.CAMERA_NAME, cv2.WINDOW_NORMAL)
					self.WINDOW = True
				cv2.imshow(self.CAMERA_NAME, self.IMAGE)
				k = cv2.waitKey(1) & 0xff
				if k == ord('q'):
					self.SHOW = False
					cv2.destroyAllWindows()
					self.IS_RUNNING = False
					break

	def _keypressHandler(self, k):
		if k == -1:
			return None
		if k == ord('q'):
			self.IS_RUNNING = False
			cv2.destroyAllWindows()
			return False
		elif k == ord('p'):
			input(f"Paused! Press enter to continue...")
			return None
		else:
			log(f"unknown keypress:{k}")

	def rdmColor(self):
		b, g, r = randint(0, 255), randint(0, 255), randint(0, 255)
		return b, g, r

	def draw_on_image(self, dets=[], img=None):
		if img is None:#if image not provided, use class attribute.
			img = self.IMAGE
		for det in dets:
			cv2.rectangle(img, (det.LEFT, det.TOP), (det.RIGHT, det.BOTTOM), self.rdmColor())
			txt_x, txt_y = det.LEFT + 50, det.BOTTOM + 50
			img = cv2.putText(img, det.NAME, (txt_x, txt_y), cv2.FONT_HERSHEY_SIMPLEX, 1, self.rdmColor(), 2, cv2.LINE_AA)
		return img


	def rdmTkColor(self):
		colors = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace', 'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff', 'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender', 'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray', 'light slate gray', 'gray', 'light gray', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue', 'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue', 'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue', 'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise', 'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green', 'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green', 'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green', 'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow', 'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown', 'sandy brown', 'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange', 'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink', 'pale violet red', 'maroon', 'medium violet red', 'violet red', 'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple', 'thistle', 'snow2', 'snow3', 'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'Slategray1', 'Slategray2', 'Slategray3', 'Slategray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3', 'cyan4', 'DarkSlategray1', 'DarkSlategray2', 'DarkSlategray3', 'DarkSlategray4', 'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4', 'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1', 'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2', 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2', 'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1', 'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'grey1', 'grey2', 'grey3', 'grey4', 'grey5', 'grey6', 'grey7', 'grey8', 'grey9', 'grey10', 'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19', 'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28', 'grey29', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37', 'grey38', 'grey39', 'grey40', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47', 'grey48', 'grey49', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56', 'grey57', 'grey58', 'grey59', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65', 'grey66', 'grey67', 'grey68', 'grey69', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74', 'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey80', 'grey81', 'grey82', 'grey83', 'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey90', 'grey91', 'grey92', 'grey93', 'grey94', 'grey95', 'grey97', 'grey98', 'grey99']
		return colors[randint(0, len(colors) - 1)]
