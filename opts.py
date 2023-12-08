import os
import pickle

def get_known_encodings(datfile=None):
	if datfile is None:
		datfile = os.path.join(os.path.expanduser("~"), '.np', 'nv', 'nv_known_faces.dat')
	with open(datfile, 'rb') as f:
		all_encodings = pickle.load(f)
		f.close()
	return all_encodings

def get_default_options():
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
	conf['OPTS'] = opts
	config().write(conf)
	return opts
