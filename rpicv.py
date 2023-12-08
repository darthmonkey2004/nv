#!/usr/bin/python3


#'camera', 'camera_config', 'camera_configuration', 'camera_controls', 'camera_ctrl_info', 'camera_idx', 'camera_manager', 'camera_properties'
import cv2
from picamera2 import Picamera2
import threading
from random import randint

class picv():
    def __init__(self, hflip=True, vflip=True, start=True, show=True, negative=False):
        self.HFLIP = hflip
        self.HFLIP = vflip
        if self.HFLIP or self.HFLIP:
                self.FLIP_IMAGE = True
        else:
                self.FLIP_IMAGE = False
        self.show = show
        self.NEGATIVE = negative
        self.CONTRAST = 1
        self.BRIGHTNESS = 1
        self.FACE_DETECTOR = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.COMMAND = None
        self.CAMERA = Picamera2()
        self.CAMERA.vflip = self.HFLIP
        self.CAMERA.hflip = self.HFLIP
        self.CAMERA.contrast = self.CONTRAST
        self.CONFIG = self.CAMERA.create_preview_configuration(main={"format": 'XRGB8888', "size": (1024, 768)})
        self.CAMERA.configure(self.CONFIG)
        self.RECT = None

        if start:
            self.start()

    def read(self):
        try:
            self.IMAGE = self.CAMERA.capture_array()
            return True, self.IMAGE
        except Exception as e:
            print(f"Error reading capture: {e}")
            return False, None

    def rdmColor(self):
        b, g, r = randint(0, 255), randint(0, 255), randint(0, 255)
        return b, g, r
            

    def loop(self):
        cv2.startWindowThread()
        self.CAMERA.start()
        self.run = True
        while self.run:
            ret, img = self.read()
            if not ret:
                print(f"Couldn't get image! Breaking...")
                cv2.destroyAllWindows()
                break
            self.IMAGE = self.adjust(img, brightness=self.BRIGHTNESS, contrast=self.CONTRAST, negative=self.NEGATIVE)
            if self.FLIP_IMAGE:
                if self.HFLIP and self.HFLIP:
                    f = -1
                elif self.HFLIP and not self.HFLIP:
                    f = 0
                elif not self.HFLIP and self.HFLIP:
                    f = 1
            else:
                f = None
            if f is not None:
                self.IMAGE = cv2.flip(self.IMAGE, f)
            self.GREY = cv2.cvtColor(self.IMAGE, cv2.COLOR_BGR2GRAY)
            self.FACES = self.FACE_DETECTOR.detectMultiScale(self.GREY, 1.1, 5)
            for (x, y, w, h) in self.FACES:
                l, t, r, b = x, y, x+w, y+h
                self.RECT = l, t, r, b
                cv2.rectangle(self.IMAGE, (l, t), (r, b), self.rdmColor())
            if self.show:
                cv2.imshow("Camera", self.IMAGE)
                k = cv2.waitKey(1)
                if ord('q') == k:
                        cv2.destroyAllWindows()
                        break
            else:
                    try:
                        cv2.destroyAllWindows()
                    except:
                        pass
            if self.COMMAND is not None:
                val = self.COMMAND.split('=')[1]
                print("Value:", val)
                if 'contrast' in self.COMMAND:
                        self.CONTRAST = round(float(val), 1)
                        print("set contrast:", self.CONTRAST)
                if 'brightness' in self.COMMAND:
                        self.BRIGHTNESS = int(val)
                        print("Set brightness:", self.BRIGHTNESS)
                if 'negative' in self.COMMAND:
                        self.NEGATIVE = bool(val)
                        print("Set negative:", self.NEGATIVE)
                self.COMMAND = None

    def start(self):
            self.t = threading.Thread(target=self.loop)
            self.t.setDaemon(True)
            self.t.start()
            print("Capture thread started!")
                        

#    def adjustAbs(self, img=None, brightness=None, contrast=None):
#            if brightness is not None:
#                    self.BRIGHTNESS = brightness
#            if contrast is not None:
#                    self.CONTRAST = contrast
#            if img is None:
#                    img = self.IMAGE
#            self.IMAGE = cv2.convertScaleAbs(img, alpha=self.BRIGHTNESS, beta=self.CONTRAST)
#            return self.IMAGE

    def adjust(self, img=None, brightness=None, contrast=None, negative=None):
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
                self.IMAGE = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
                self.IMAGE = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.IMAGE = cv2.addWeighted(self.IMAGE, self.CONTRAST, self.IMAGE, 0, self.BRIGHTNESS)
        return self.IMAGE


if __name__ == "__main__":
    picv = picv(start=True, show=True)
    while True:
            pass
