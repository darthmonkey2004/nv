import threading
from random import randint
from logger import logger
import time
import requests
import base64
import os
import keyring
import getpass
from conf import config

log = logger().log
def get_user_input(txt="Insert text string here:"):
	txtline = [sg.Text(txt)]
	inputline = [sg.Input("", key="-INPUT-")]
	btnsline = [sg.Button("Cancel"), sg.Button("Ok")]
	layout = []
	layout.append(txtline)
	layout.append(inputline)
	layout.append(btnsline)
	win = sg.Window(title="moo", layout=layout)
	run = True
	output = None
	while run:
		event, values = win.read()
		if event == 'Cancel':
			win.close()
			run  = False
			break
		elif event == 'Ok':
			output = values['-INPUT-']
			win.close()
			run = False
			break
	return output

class ptz():
	def __init__(self, camera_id, **args):
		self.CONFIG = config().read()
		self.CAMERA_ID = camera_id
		self.PRESETS = self.CONFIG['CAMERAS'][self.CAMERA_ID]['PTZ']['PRESETS']
		self.CAMERA_NAME = f"Camera_{self.CAMERA_ID}"
		self._set_args(args)
		try:
			user = self.USER
		except:
			#if class attribute not set, set from environment variable.
			self.USER = os.environ["USER"]
		settings = self.CONFIG['CAMERAS'][self.CAMERA_ID]['PTZ']
		if settings == {}:
			self.SETTINGS = self._init_ptz()
			self.CONFIG['CAMERAS'][self.CAMERA_ID]['PTZ'] = self.SETTINGS
			config().write(self.CONFIG)
		else:
			self.SETTINGS = settings
		self.BASEURL = self.SETTINGS['BASEURL']
		self.CAMERA_IP = self.SETTINGS['CAMERA_IP']
		self.HEADERS = None

	def _init_ptz(self):
		keys = ['BASEURL', 'CAMERA_IP']
		settings = {}
		val = get_user_input("Enter Camera IP:")
		if val == '':
			log(f"No value provided! Using None...")
			val = None
		settings['CAMERA_IP'] = val
		settings['BASEURL'] = f"http://{settings['CAMERA_IP']}/web/cgi-bin/hi3510"
		return settings

	def _set_args(self, args):
		for k in args.keys():
			v = args[k]
			self.__dict__[k] = v

	def _store_creds(self, user=None, pw=None):
		if user is None:
			user = self.USER
		if pw is None:
			pw = getpass.getpass("Enter password:")
		try:
			keyring.set_password(service_name=self.CAMERA_NAME, username=user, password=pw)
		except Exception as e:
			log(f"Error storing credentials: {e}")
			return False
		return True
	
	def _get_creds(self, user=None):
		if user is None:
			user = self.USER
		else:
			#set class attribute if provided.
			self.USER = user
		pw = keyring.get_password(service_name=self.CAMERA_NAME, username=self.USER)
		return pw

	def _get_auth_header(self, user=None, pw=None):
		error = None
		fail = False
		if user is None:
			user = self.USER
		if pw is None:
			try:
				pw = self._get_creds(user)
				if pw is None:
					error = f"Pw stored is None!  Weirdo..."
					fail = True
				else:
					pass
			except Exception as e:
				fail = True
				error = e
		if fail:
			log(f"Error getting credentials: {error}")
			pw = getpass.getpass("Enter password: ")
			self._store_creds(user=user, pw=pw)
		authstr = base64.b64encode(f"{user}:{pw}".encode('UTF-8')).decode()
		header = {}
		header['Authorization'] = f"Basic {authstr}"
		return header
		
	def step(self, direction=None, steps=1):
		if direction is None:
			log(f"No pan direction provided!")
			return False
		if direction not in ['left', 'right', 'up', 'down']:	
			log(f"Cannot pan {direction}!")
			return False
		url = f"{self.BASEURL}/yt{direction}.cgi?"
		for i in range(0, steps):
			self._get(url)
			#time.sleep(1)


	def set_ptz_speed(self, speed=0):
		url = f"{self.BASEURL}/param.cgi?cmd=setmotorattr&-tiltspeed={speed}&-panspeed={speed}"
		return self._get(url)


	def set_cam_prop(self, key, val):
		props = ['brightness', 'contrast', 'saturation', 'sharpness', 'speed']
		if key not in props:
			log(f"Error setting camera property - unknown key {key}")
			return False
		if key == 'speed':
			#if key is speed, execute and return early.
			return self.set_ptz_speed(speed=val)
		#if key is param, continue.
		url = f"{self.BASEURL}/param.cgi?cmd=setimageattr&-image_type=0&-{key}={val}"
		try:
			self._get(url)
		except Exception as e:
			log(f"Error setting camera property -{e}")
			return False
		return True


	def get_params(self):
		d = {}
		data = self._get(f"{self.BASEURL}/param.cgi?cmd=getvencattr&-chn=11&cmd=getvencattr&-chn=12&cmd=getsetupflag&cmd=getvideoattr&cmd=getimageattr&cmd=getinfrared&cmd=getserverinfo&cmd=getmotorattr&cmd=getinfrared&cmd=getrtmpattr")
		items = [item.split(' ')[1].split(';')[0] for item in data.splitlines()]
		for item in items:
			k = item.split('=')[0]
			v = item.split('"')[1]
			d[k] = v
		return d

	def preset_set(self, number=0):
		return self._get(f"{self.BASEURL}/param.cgi?cmd=preset&-act=set&-status=1&-number={number}")

	def preset_go(self, number=0):
		return self._get(f"{self.BASEURL}/param.cgi?cmd=preset&-act=goto&-number={number}")

	def _get(self, url):
		if self.HEADERS is None:
			self.HEADERS = self._get_auth_header()
		r = requests.get(url, headers=self.HEADERS)
		if r.status_code == 200:
			return r.text
		else:
			log(f"Error sending request: Bad Code ({r.status_code})")
			return r.text

	def tour(self, wait=7):
		self.run = True
		while self.run:
			for preset in self.PRESETS:
				self.preset_go(preset)
				time.sleep(wait)
			if not self.run:
				break

	def start_tour(self):
		self.TOUR_THREAD = threading.Thread(target=self.tour)
		self.TOUR_THREAD.setDaemon(True)
		self.TOUR_THREAD.start()

	def stop_tour(self):
		self.run = False
		print(f"Stopping tour...")

	def save_presets(self, presets=None):
		if presets is None:
			presets = self.PRESETS
		self.CONFIG['CAMERAS'][self.CAMERA_ID]['PTZ']['PRESETS'] = presets
		config().write(self.CONFIG)

	def load_presets(self):
		self.PRESETS = self.CONFIG['CAMERAS'][self.CAMERA_ID]['PTZ']['PRESETS']
		return self.PRESETS
