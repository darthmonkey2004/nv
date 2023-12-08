from camera import camera
from ptz import *
import os
from random import randint
import PySimpleGUI as sg
from conf import config


class nvui():
	def __init__(self, noinit=False):
		self.new_ptz = ptz
		self.layout = []
		self.rows = []
		self.column = []
		self.tabs = []
		print("reading config...")
		self.CONF = config().read()
		ids = list(self.CONF['CAMERAS'].keys())
		self.CAMERA_KEYS = []
		for camera_id in ids:
			self.CAMERA_KEYS.append(f"-CAMERA_{camera_id}-")
		print(f"Keys:{self.CAMERA_KEYS}")
		self.PTZS = {}
		self.CAMERAS = {}
		self.ACTIVE_TAB = None
		if not noinit:
			for camera_id in self.CONF['CAMERAS']:
				print(f"Initializing camera: {camera_id}")
				self._init_camera(camera_id=camera_id, show=False, process=None)

	def add_camera(self):
		newdata = {}
		newdata['SRC'] = 'x11://0'
		newdata['TYPE'] = 'screengrab'
		newdata['HAS_PTZ'] = False
		newdata['PTZ'] = {}
		newdata['PROCESS'] = None
		filename = os.path.join(os.path.expanduser("~"), "nv", "offline.png")
		self.add_element(sg.Image(filename=filename, enable_events=True))
		self.add_row()
		self.add_element(sg.Text("Camera source string:"))
		self.add_element(sg.Input("", key="-SET_SRC-", enable_events=True, change_submits=True))
		self.add_element(sg.Button("Test preview!"))
		self.add_row()
		self.add_element(sg.Text("Has PTZ Control:"))
		self.add_element(sg.Checkbox("", default=False, enable_events=True, change_submits=True, key="-SET_HAS_PTZ"))
		self.add_element(sg.Text("PTZ Url:"))
		self.add_element(sg.Input("", key="-SET_PTZ_URL-", enable_events=True, change_submits=True))
		self.add_row()
		types=['screengrab', 'cv2', 'imagezmq', 'rpi']
		self.add_element(sg.Text("Capture type:"))
		self.add_element(sg.Combo(values=types, default_value='cv2', key="-SET_CAP_TYPE-", enable_events=True, change_submits=True))
		self.add_element(sg.Text("Image processing method:"))
		self.add_element(sg.Combo(values=['None', 'face_detect', 'object_detect', 'recognize'], default_value='None', key='-SET_PROC_TYPE-', enable_events=True, change_submits=True))
		self.add_element(sg.Text("Active detection library:"))
		self.add_element(sg.Combo(values=['cv2', 'dlib'], default_value='cv2', key='-SET_DETECTION_PROVIDER-', enable_events=True, change_submits=True))
		self.add_row()
		self.add_element(sg.Button("Cancel"))
		self.add_element(sg.Button("Ok"))
		self.add_row()
		win = sg.Window(title='Add Camera', layout=self.rows)
		run = True
		while run:
			event, values = win.read()
			if event == sg.WINDOW_CLOSED:
				run = False
				break
			elif event == 'Cancel' or event == 'Ok':
				win.close()
			elif event == "-SET_SRC-":
				newdata['SRC'] = values[event]
				print("Source set:", newdata['SRC'])
			elif event == "-SET_CAP_TYPE-":
				newdata['TYPE'] = values[event]
				print("Capture type set:", newdata['TYPE'])
			elif event == "-SET_HAS_PTZ-":
				newdata['HAS_PTZ'] = values[event]
				print("PTZ Flag toggled:", newdata['HAS_PTZ'])
			elif event == '-SET_PROC_TYPE-':
				newdata['PROCESS'] = values[event]
				print("Process type set:", newdata['PROCESS'])
		return newdata

	def get_camera_id(self, src):
		srcs = {}
		for camera_id in self.CONF['CAMERAS']:
			srcs[camera_id] = self.CONF['CAMERAS'][camera_id]['SRC']
		if src in list(srcs.values()):
			return list(self.CONF['CAMERAS'].keys())[list(srcs.values()).index(src)]
		else:
			last = len(list(self.CONF['CAMERAS'].keys())) - 1
			return list(self.CONF['CAMERAS'].keys())[last] + 1


	def _init_camera(self, ptzobj=None, camera_id=0, camobj=None, show=True, process=None):
		if self.CONF['CAMERAS'][camera_id]['HAS_PTZ']:
			if ptzobj is None:
				self.PTZS[camera_id] = self.new_ptz(camera_id=camera_id)
			else:
				self.PTZS[camera_id] = ptzobj
		else:
				pass
		if camobj is None:
			self.CAMERAS[camera_id] = camera(camera_id=camera_id, show=show, process=self.CONF['CAMERAS'][camera_id]['PROCESS'])
		else:
			self.CAMERAS[camera_id] = camobj
		self.CAMERAS[camera_id].writeThumbnail()

	def add_row(self, rows=None, column=None):
		if rows is None:
			rows = self.rows
		if column is None:
			column = self.column
		if type(column) != list:
			column = [column]
		rows.append(column)
		self.column = []
		self.rows = rows
		return rows

	def add_element(self, element, column=None):
		if column is None:
			column = self.column
		column.append(element)
		self.column = column
		return column

	def add_to_tab(self, title, rows=None):
		if rows is None:
			rows = self.rows
		self.rows = []#blank rows list becuse we're using it in a container
		if title == 'Overview':
			self.tabs.append(sg.Tab(title, layout=rows, key = f"-TAB_{title}-", tooltip = title, expand_x = False, expand_y = False, element_justification = "center"))
		else:
			self.tabs.append(sg.Tab(f"Camera_{title}", layout=rows, key = f"-TAB_CAMERA_{title}-", tooltip = f"Camera_{title}", expand_x = False, expand_y = False, element_justification = "center"))
		return self.tabs

	def add_tab_to_grp(self, tabs=None):
		if tabs is None:
			tabs = self.tabs
		layout = []
		layout.append(tabs)
		layout2 = []
		layout2.append([sg.TabGroup(layout=layout, tab_location = 'bottom', change_submits = True, enable_events = True, key = f"-TABGRP_CAMERAS-", size = (None, None), tooltip = f"Camera Tabs", expand_x = False, expand_y = False)])
		self.layout = layout2
		return layout2

	def get_camera_ui(self, title):
		if title != "Overview":
			self.add_element(sg.Button('up'))
			self.add_row()
			self.add_element(sg.Button('left'))
			self.add_element(sg.Button('right'))
			self.add_row()
			self.add_element(sg.Button('down'))
			self.add_row()
			self.add_element(sg.Text("Goto/Set presets:"))
			self.add_element(sg.Input(key='-SET_PRESET-', enable_events=True))
			self.add_element(sg.Button('Goto'))
			self.add_element(sg.Button('Set'))
			self.add_row()
			self.add_element(sg.Text('Pan/Tilt speed:'))
			self.add_element(sg.Combo(['0', '1', '2'], default_value = '0', size = (None, None), auto_size_text = True, change_submits = True, enable_events = True, key = '-SET_SPEED-', tooltip = "Set ptz pan/tilt speed:"))
			self.add_element(sg.Button('Start Tour'))
			self.add_element(sg.Button('Stop Tour'))
			self.add_row()
			self.add_element(sg.Combo(['None', 'face_detect', 'object_detect', 'recognize'], default_value = 'None', size = (None, None), auto_size_text = True, change_submits = True, enable_events = True, key = "-SET_PROCESS-", tooltip = "Set process type:"))
			self.add_row()
			self.add_element(sg.Slider(range = (-127, 127), default_value = 1, resolution = 1, tick_interval = 1, orientation = 'h', change_submits = True, enable_events = True, size = (None, None), font = None, key = "-SET_CONTRAST-", expand_x = True, expand_y = False, tooltip = "Adjust contrast level"))
			self.add_row()
			self.add_element(sg.Slider(range = (-250, 250), default_value = 1, resolution = 1, tick_interval = 1, orientation = 'h', change_submits = True, enable_events = True, size = (None, None), font = None, key = "-SET_BRIGHTNESS-", expand_x = True, expand_y = False, tooltip = "Adjust contrast level"))
			self.add_row()
			self.add_element(sg.Checkbox("Negative", default = False, size = (None, None), auto_size_text = True, change_submits = True, enable_events = True, key = '-NEGATIVE-', tooltip = "Add Negative colorization effect"))
			self.add_element(sg.Checkbox("GRAY", default = False, size = (None, None), auto_size_text = True, change_submits = True, enable_events = True, key = '-GRAY-', tooltip = "Add grayscale effect"))
			self.add_row()
			self.add_element(sg.Button('Close'))
			self.add_row()
			tabs = self.add_to_tab(title=title)
			return tabs
		else:
			conf = config().read()

			for camera_id in conf['CAMERAS']:
				thumbpath = os.path.join(os.path.expanduser("~"), 'nv', f"Camera_{camera_id}.png")
				if not os.path.exists(thumbpath):
					thumbpath = os.path.join(os.path.expanduser("~"), 'nv', "offline.png")
				self.add_element(sg.Image(filename=thumbpath, key=f"-OVERVIEW_{camera_id}-", enable_events=True, expand_x=True))
				self.add_row()
			tabs = self.add_to_tab(title=title)
			return tabs

	def window(self):
		thumbpath = os.path.join(os.path.expanduser("~"), 'nv', "offline.png")
		conf = config().read()
		menu_def = [['File', ['New Camera', 'Close']]]
		self.add_element(sg.Menu(menu_definition=menu_def, size = (None, None), tearoff = False, key = "-MENU-"))
		for camera_id in conf['CAMERAS']:
			self.add_element(sg.Image(filename=thumbpath, key=f"-CAMERA_{camera_id}-", enable_events=True))
			self.add_row()
			tabs = self.get_camera_ui(title=camera_id)
		tabs = self.get_camera_ui(title="Overview")
		layout = self.add_tab_to_grp(tabs=tabs)
		win = sg.Window(title='title', layout=self.layout, finalize=True)
		return win

	def loop(self, win):
		self.ACTIVE_TAB = None
		self.WINDOW = win
		self.CURRENT_CAMERA_ID = 0
		run = True		
		while run:
			if self.ACTIVE_TAB != None and self.ACTIVE_TAB != '-TAB_Overview-':
				camera_id = int(self.ACTIVE_TAB.split('CAMERA_')[1].split('-')[0])
				cam = self.CAMERAS[camera_id]
				img = cam.read()
				cam.writeThumbnail(img=img)
				self.WINDOW[f"-CAMERA_{camera_id}-"].update(cam.THUMBNAIL)
			else:
				for camera_id in self.CAMERAS:
				
					self.CAMERAS[camera_id].writeThumbnail()
					self.WINDOW[f"-OVERVIEW_{camera_id}-"].update(self.CAMERAS[camera_id].THUMBNAIL)
			event, values = self.WINDOW.read(timeout=1)
			if event == '__TIMEOUT__':
				pass
			elif event == '-TABGRP_CAMERAS-':
				self.ACTIVE_TAB = values[event]
				#print(f"Tab selected: {self.ACTIVE_TAB}")
			elif event == sg.WINDOW_CLOSED:
				run = False
				break
			elif event in self.CAMERA_KEYS:
					print("Camera monitor clicked!")
					self.CURRENT_CAMERA_ID = int(event.split('_')[1].split('-')[0])
					print(f"loading viewer for camera {camera_id}...")
					cam = self.CAMERAS[camera_id]
					cam.SHOW=True
					self.WINDOW[event].update(cam.THUMBNAIL)
					print("loaded!")
			elif event in ['left', 'right', 'down', 'up']:
				self.PTZS[self.CURRENT_CAMERA_ID].step(direction=event, steps=1)
			elif event == '-SET_PRESET-':
				pass
			elif event == 'Goto':
				self.PTZS[self.CURRENT_CAMERA_ID].preset_go(values['-SET_PRESET-'])
				#print(f"Moved to position {values['-SET_PRESET-']}")
			elif event == 'Set':
				self.PTZS[self.CURRENT_CAMERA_ID].preset_set(values['-SET_PRESET-'])
				#print(f"Preset selected: {values['-SET_PRESET-']}")
			elif event == '-SET_CONTRAST-':
				self.CAMERAS[self.CURRENT_CAMERA_ID].CONTRAST = values['-SET_CONTRAST-']
				print(f"Contrast set: {self.CAMERAS[self.CURRENT_CAMERA_ID].CONTRAST}")
			elif event == '-SET_BRIGHTNESS-':
				self.CAMERAS[self.CURRENT_CAMERA_ID].BRIGHTNESS = values['-SET_BRIGHTNESS-']
				print(f"Brightness set: {self.CAMERAS[self.CURRENT_CAMERA_ID].BRIGHTNESS}")
			elif event == '-NEGATIVE-':
				self.CAMERAS[self.CURRENT_CAMERA_ID].NEGATIVE = values[event]
				print(f"Set effect: Negative({self.CAMERAS[self.CURRENT_CAMERA_ID].NEGATIVE})")
			elif event == '-GRAY-':
				self.CAMERAS[self.CURRENT_CAMERA_ID].GRAY = values[event]
				print(f"Set effect: Grayscale({self.CAMERAS[self.CURRENT_CAMERA_ID].GRAY})")
			elif event == '-SET_PROCESS-':
				proc = values[event]
				if proc == 'None':
					proc = None
				self.cam.PROCESS = proc
				self.CONF['CAMERAS'][self.CAMERA_ID]['PROCESS'] = self.cam.PROCESS
				self.CONF['OPTIONS']['CV_TYPE'] = self.cam.PROCESS
				print(f"Set process type: {self.cam.PROCESS}")
				config().write(self.CONF)
			elif event == '-SET_SPEED-':
				self.PTZS[self.CURRENT_CAMERA_ID].set_ptz_speed(values[event])
				print(f"Set ptz speed: {values[event]}")
			elif event == 'Start Tour':
				self.PTZS[self.CURRENT_CAMERA_ID].start_tour()
				print(f"Tour started!")
			elif event == 'Stop Tour':
				self.PTZS[self.CURRENT_CAMERA_ID].stop_tour()
			elif event == 'New Camera':
				self.new_camera()
				print(f"Please restart software!")
				input("Press enter to quit...")
				exit()
			elif event == 'Close':
				win.close()
			else:
				pass
				#print(event, values)


	def start(self):
		self.WINDOW = self.window()
		self.WINDOW["-TAB_Overview-"].select()
		self.loop(win=self.WINDOW)

	def new_camera(self):
		newdata = self.add_camera()
		src = newdata['SRC']
		camera_id = self.get_camera_id(src=src)
		self.CONF['CAMERAS'][camera_id] = newdata
		config().write(self.CONF)

if __name__ == "__main__":
	ui = nvui()
	ui.start()
