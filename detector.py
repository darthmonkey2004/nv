import numpy as np
from detection import detection
import os
import cv2
import pickle
from conf import config

def constrain_box(img, l, t, r, b):
	h, w, c = img.shape
	if t <= 0:
		t = 10
	elif t >= h:
		t = h - 10
	if b <= 0:
		b = 10
	elif b >= h:
		b = h - 10
	if r <= 0:
		r = 10
	elif r >= w:
		r = w - 10
	if l <= 0:
		l = 10
	elif l >= w:
		l = w - 10
	return l, t, r, b

class detector():
	def __init__(self, read_db=False, target_confidence=0.5, cv_type='face_detect', default_cv_lib='cv2', dlib_fd_model='hog', dlib_fd_upsamples=1, cam=None):
		self.CONF = config().read()
		self.set_attributes()
		self.TARGET_CONFIDENCE = target_confidence
		self.CV_TYPE = cv_type
		self.DEFAULT_CV_LIB = default_cv_lib
		self.PROCESS = f"{self.CV_TYPE}_{self.DEFAULT_CV_LIB}"
		self.DATA_DIR = os.path.join(os.path.expanduser("~"), '.nv')
		self.CASCADEFILE = os.path.join(self.DATA_DIR, 'haarcascade_frontalface_default.xml')
		self.faceCascade = cv2.CascadeClassifier(self.CASCADEFILE);
		self.DLIB_FD_UPSAMPLES = dlib_fd_upsamples
		self.DLIB_FD_MODEL = dlib_fd_model
		if read_db:
			self.FACE_ENCODINGS = self.get_known_encodings()
		if cam is not None:
			self.IMAGE = cam.IMAGE
		else:
			self.IMAGE = None
		self.net = cv2.dnn.readNetFromCaffe(self.OBJECT_DETECT_PROTOTXT, self.OBJECT_DETECT_MODEL)


	def set_attributes(self):
		for k in self.CONF['OPTIONS']:
			v = self.CONF['OPTIONS'][k]
			self.__dict__[k] = v

	def detect(self, img, _type='detect_object', provider='cv2'):
		if _type == 'object_detect':
			return self.object_detect(imgpath=img)
		elif _type == 'face_detect':
			if provider == 'cv2':
				return self.face_detect_cv2(img=img)
			elif provider == 'dlib':
				return self.face_detect_dlib(imgpath=img)
		elif _type == 'recognize':
			if provider == 'cv2':
				return self.recognize_cv2(imgpath=img)
			elif provider == 'dlib':
				return self.recognize_dlib(img=img)

	def get_known_encodings(self):
		datfile = os.path.join(os.path.expanduser("~"), '.np', 'nv', 'nv_known_faces.dat')
		with open(datfile, 'rb') as f:
			all_encodings = pickle.load(f)
			f.close()
		return all_encodings
		
	def face_detect_cv2(self, img=None):
		if img is None:
			img = self.IMAGE
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		print(img.shape)
		faces = self.faceCascade.detectMultiScale(gray, scaleFactor=self.CV2_FD_SCALE_FACTOR, minNeighbors=self.CV2_FD_MIN_NEIGHBORS, minSize=self.CV2_FD_MIN_SIZE)
		dets = []
		for (x,y,w,h) in faces:
			box = x, y ,x+w, y+h
			name = 'Unrecognized Face'
			confidence = None
			det = detection(img=img, label=name, rect=box, confidence=confidence)
			dets.append(det)
		return dets


	def face_detect_dlib(self, imgpath):
		if type(imgpath) == str:
			img = cv2.imread(imgpath)
		else:
			img = imgpath
		img = imutils.resize(img, width=400)
		if img is None:
			return (None, None, None)
		self.box = fr_dlib.face_locations(img, upsamples=self.DLIB_FD_UPSAMPLES, model=self.DLIB_FD_MODEL)
		if self.box is None:
			return (None, None, None)
		self.name = "Detected Face"
		dets = []
		try:
			for box in self.box:
				det = detection(img=img, label=self.name, rect=box)
				dets.append(det)
		except:
			dets = []
		return dets


	def recognize_cv2(self, imgpath, scaleFactor=None, minNeighbors=None, sizeModifier=None):
		if scaleFactor is None:
			scaleFactor = self.CV2_FD_SCALE_FACTOR
		if minNeighbors is None:
			minNeighbors = self.CV2_FD_MIN_NEIGHBORS
		if sizeModifier is None:
			sizeModifier = self.CV2_FD_SIZE_MODIFIER
		dets = []
		if type(imgpath) == str:
			img = cv2.imread(imgpath)
		else:
			img = imgpath
		(self.H, self.W) = img.shape[:2]
		minW = sizeModifier*self.W
		minH = sizeModifier*self.H
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize = (int(minW), int(minH))) 
		for(x,y,w,h) in faces:
			l, t, r, b = x, y, x+w, y+h
			_id, confidence = self.cv2_recognizer.predict(gray[t:b,l:r])
			if confidence < 100:
				name = self.cv2_known_names[_id]
				confidence = int(f"{format(round(100 - confidence))}")
				det = detection(img=img, label=name, rect=(l, t, r, b), confidence=confidence)
				dets.append(det)
		return dets

	def get_matches(self, img, tolerance=None):
		if tolerance is not None:
			#a good start is 0.8
			tolerance = self.DLIB_FR_TOLERANCE
		if type(img) is str:
			img = cv2.imread(img)
		boxes = fr_dlib.face_locations(img)
		dets = fr_dlib.face_encodings(img, boxes)
		matches = {}
		for box in boxes:
			encodings = list(self.FACE_ENCODINGS.values())
			self.encodings = np.array(encodings, dtype=object)
			for test in dets:
				idx = -1
				for landmark in list(encodings):
					idx += 1
					dist = round(float(np.linalg.norm(landmark - test)), 2)
					print(dist)
					tolerance = float(tolerance)
					if dist <= tolerance:
						name = list(self.FACE_ENCODINGS.keys())[idx].split('_')[0]
						matches[dist] = {}
						matches[dist]['idx'] = idx
						matches[dist]['name'] = name
						matches[dist]['dist'] = dist
						matches[dist]['box'] = box
		return matches

	def recognize_dlib(self, img, tolerance=None):
		if tolerance is not None:
			#a good start is 0.8
			tolerance = self.DLIB_FR_TOLERANCE
		matches = self.get_matches(img, tolerance)
		out = []
		if matches != {}:
			best = sorted(matches.keys())[0]
			dist = matches[best]['dist']
			confidence = 1 - dist * 100
			c = float(str(confidence).split('-')[1])
			box = matches[best]['box']
			name = matches[best]['name']
			det = detection(img=img, label=name, rect=box, confidence=c)
			out.append(det)
			#o = name, box, c
			#out.append(o)
		return out

	def object_detect(self, imgpath, targets=None, target_confidence=None):
		if target_confidence is None:
			target_confidence = self.TARGET_CONFIDENCE
		if targets is not None:
			targets = self.targets
		if type(imgpath) == str:
			img = cv2.imread(imgpath)
		else:
			img = imgpath
		#img = cv2.resize(fullimg, (300, 300))
		(self.H, self.W) = img.shape[:2]
		blob = cv2.dnn.blobFromImage(img, self.OBJECT_DETECT_SCALE, self.OBJECT_DETECT_INPUT_SHAPE, self.OBJECT_DETECT_MEAN, self.OBJECT_DETECT_SWAP_RB)
		self.net.setInput(blob)
		detections = self.net.forward()
		out = []
		for i in range(0, detections.shape[2]):
			confidence = float(detections[0, 0, i, 2])
			idx = int(detections[0, 0, i, 1])
			name = self.OBJECT_DETECT_CLASSES[idx]
			if name in self.OBJECT_DETECT_TARGETS and float(confidence) >= float(self.TARGET_CONFIDENCE):
				#dets = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
				dets = detections[0, 0, i, 3:7] * np.array([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
				l, t, r, b = dets.astype("int")
				l, t, r, b = constrain_box(img, l, t, r, b)
				box = (l, t, r, b)
				#o = (name, box, confidence)
				det = detection(img=img, label=name, rect=box, confidence=confidence)
				out.append(det)
				#out.append(o)
		return out

	def yolov3(self, image):
		Width = image.shape[1]
		Height = image.shape[0]
		blob = cv2.dnn.blobFromImage(image, self.yolo_scale, (416,416), (0,0,0), True, crop=False)
		self.yolo_net.setInput(blob)
		outs = self.yolo_net.forward(get_output_layers(self.yolo_net))
		class_ids = []
		confidences = []
		boxes = []
		conf_threshold = 0.5
		nms_threshold = 0.4
		for out in outs:
			for detection in out:
				scores = detection[5:]
				class_id = np.argmax(scores)
				confidence = scores[class_id]
				if confidence > 0.5:
					center_x = int(detection[0] * Width)
					center_y = int(detection[1] * Height)
					w = int(detection[2] * Width)
					h = int(detection[3] * Height)
					x = center_x - w / 2
					y = center_y - h / 2
					class_ids.append(class_id)
					confidences.append(float(confidence))
					boxes.append([x, y, w, h])
			indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
		out = []
		for i in indices:
			box = boxes[i]
			x = box[0]
			y = box[1]
			w = box[2]
			h = box[3]
			box = round(x), round(y), round(x+w), round(y+h)
			name = self.yolo_classes[class_ids[i]]
			confidence  = confidences[i]
			o = (name, box, confidence)
			out.append(o)
		return out

		def detect(self, img=None, process='face_detect_cv2'):
			if img is None:
				img = self.IMAGE
			if process is None:
					process = self.PROCESS
			if 'face_detect' in process:
				if 'cv2' in process:
					dets = self.face_detect_cv2(img=img)
				elif 'dlib' in process:
					dets = self.face_detect_dlib(imgpath=img)
			elif 'recognize' in process:
				if 'cv2' in process:
					dets = self.recognize_cv2(imgpath=img)
				elif 'dblib' in process:
					dets = self.recognize_dlib(img=img, tolerance=self.TARGET_CONFIDENCE)
			elif 'object' in process:
				dets = self.detect_object(img=img)
			else:
				log(f"Unknown process type: {process}")
				dets = []
			return dets
