import os
import pickle
import opts

class config():
	def __init__(self):
		self.DATA_DIR = os.path.join(os.path.expanduser("~"), '.nv')
		self.CONF_FILE = os.path.join(self.DATA_DIR, 'nv.conf')
		ret = self.test()
		if type(ret) == tuple:
			ret, errmsg = ret
		if ret:
			self.conf = self.read()
		else:
			self.conf = self.init_config()

	def test(self):
		if not os.path.exists(self.DATA_DIR):
			try:
				os.makedirs(self.DATA_DIR, exist_ok=True)
			except Exception as e:
				return False, e
		if not os.path.exists(self.CONF_FILE):
			try:
				self.init_config()
			except Exception as e:
				return False, e
		return True

	def read(self):
		f = open(self.CONF_FILE, 'rb')
		self.data = pickle.load(f)
		return self.data

	def write(self, data=None):
		if data is not None:
			#if data is set, update class attribute
			self.data = data
		f = open(self.CONF_FILE, 'wb')
		pickle.dump(self.data, f)
		f.close()

	def init_config(self, noopts=False):
		d = {}
		d['OPTIONS'] = {}
		d['CAMERAS'] = {}
		d['CAMERAS'][0] = {}
		d['CAMERAS'][0]['SRC'] = 'rtsp://192.168.1.8/12'
		d['CAMERAS'][0]['TYPE'] = 'cv2'
		d['CAMERAS'][0]['HAS_PTZ'] = False
		d['CAMERAS'][0]['PTZ'] = {}
		d['CAMERAS'][0]['PROCESS'] = 'object_detect'
		d['CAMERAS'][0]['PTZ']['PRESETS'] = [0, 1, 2]
		if not noopts:
			d['OPTIONS'] = self.get_default_options()
		else:
			d['OPTIONS'] = {}
		self.conf = d
		self.write(self.conf)
		return self.conf
		
	def get_default_options(self):
		opts = {}
		opts['DETECT_OBJECT_TARGETS'] =  ['person', 'cat', 'horse', 'truck', 'dog', 'car', 'motorbike']
		opts['DETECT_OBJECT_CLASSES'] = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
		opts['TARGET_CONFIDENCE'] = 0.5
		opts['DLIB_FR_TOLERANCE'] = 0.8
		opts['CV_TYPE'] = 'face_detect'
		opts['DEFAULT_CV_LIB'] = 'cv2'
		opts['DLIB_FD_MODEL'] = 'hog'
		opts['DLIB_FD_UPSAMPLES'] = 1
		opts['PROCES'] = f"{opts['CV_TYPE']}_{opts['DEFAULT_CV_LIB']}"
		opts['DATA_DIR'] = os.path.join(os.path.expanduser("~"), '.nv')
		opts['CASCADEFILE'] = os.path.join(opts['DATA_DIR'], 'haarcascade_frontalface_default.xml')
		opts['CV2_FD_SCALE_FACTOR'] = 1.2
		opts['CV2_FD_MIN_NEIGHBORS'] = 5
		opts['CV2_FD_MIN_SIZE'] = (20, 20)
		opts['CV2_FD_SIZE_MODIFIER'] = 0.1
		opts['OBJECT_DETECT_SCALE'] = 0.01
		opts['OBJECT_DETECT_INPUT_SHAPE'] = (300, 300)
		opts['OBJECT_DETECT_MEAN'] = (127.5, 127.5, 127.5)
		opts['OBJECT_DETECT_SWAP_RB'] = True
		opts['OBJECT_DETECT_PROTOTXT'] = os.path.join(opts['DATA_DIR'], 'MobileNetSSD_deploy.prototxt')
		opts['OBJECT_DETECT_MODEL'] = os.path.join(opts['DATA_DIR'], 'MobileNetSSD_deploy.caffemodel')
		opts['OBJECT_DETECT_CLASSES'] =  ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
		opts['OBJECT_DETECT_TARGETS'] =  ['person', 'cat', 'horse', 'truck', 'dog', 'car', 'motorbike']
		try:
			opts['FACE_ENCODINGS'] = get_known_encodings()
		except:
			opts['FACE_ENCODINGS'] = {}
		conf = self.init_config(noopts=True)
		conf['OPTIONS'] = opts
		self.write(conf)
		return opts	

def get_known_encodings(datfile=None):
	if datfile is None:
		datfile = os.path.join(os.path.expanduser("~"), '.np', 'nv', 'nv_known_faces.dat')
	with open(datfile, 'rb') as f:
		all_encodings = pickle.load(f)
		f.close()
	return all_encodings

	
