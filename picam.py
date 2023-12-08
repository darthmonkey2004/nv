#!/usr/bin/python3


#'camera', 'camera_config', 'camera_configuration', 'camera_controls', 'camera_ctrl_info', 'camera_idx', 'camera_manager', 'camera_properties'
import cv2
from picamera2 import Picamera2
import threading
from random import randint
import time

class rpi():
    def __init__(self, hflip=True, vflip=True, start=True, show=True, negative=False):
        self.IS_RUNNING = False
        self.HFLIP = hflip
        self.HFLIP = vflip
        if self.HFLIP or self.HFLIP:
                self.FLIP_IMAGE = True
        else:
                self.FLIP_IMAGE = False
        self.SHOW = show
        self.NEGATIVE = negative
        self.CONTRAST = 0.5
        self.BRIGHTNESS = -15
        self.COMMAND = None
        self.CAMERA = Picamera2()
        self.release = self.CAMERA.close
        self.CAMERA.vflip = self.HFLIP
        self.CAMERA.hflip = self.HFLIP
        self.CAMERA.contrast = self.CONTRAST
        self.CONFIG = self.CAMERA.create_preview_configuration(main={"format": 'XRGB8888', "size": (1024, 768)})
        self.CAMERA.configure(self.CONFIG)
        if start:
            self.start()
            time.sleep(3)

    def read(self):
        try:
            self.IMAGE = self.CAMERA.capture_array()
            return True, self.IMAGE
        except Exception as e:
            print(f"Error reading capture: {e}")
            return False, None



    def rdmTkColor(self):
        colors = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace', 'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff', 'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender', 'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray', 'light slate gray', 'gray', 'light gray', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue', 'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue', 'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue', 'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise', 'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green', 'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green', 'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green', 'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow', 'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown', 'sandy brown', 'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange', 'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink', 'pale violet red', 'maroon', 'medium violet red', 'violet red', 'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple', 'thistle', 'snow2', 'snow3', 'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'Slategray1', 'Slategray2', 'Slategray3', 'Slategray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3', 'cyan4', 'DarkSlategray1', 'DarkSlategray2', 'DarkSlategray3', 'DarkSlategray4', 'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4', 'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1', 'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2', 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2', 'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1', 'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'grey1', 'grey2', 'grey3', 'grey4', 'grey5', 'grey6', 'grey7', 'grey8', 'grey9', 'grey10', 'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19', 'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28', 'grey29', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37', 'grey38', 'grey39', 'grey40', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47', 'grey48', 'grey49', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56', 'grey57', 'grey58', 'grey59', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65', 'grey66', 'grey67', 'grey68', 'grey69', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74', 'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey80', 'grey81', 'grey82', 'grey83', 'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey90', 'grey91', 'grey92', 'grey93', 'grey94', 'grey95', 'grey97', 'grey98', 'grey99']
        return colors[randint(0, len(colors) - 1)]


    def loop(self):
        cv2.startWindowThread()
        self.CAMERA.start()
        self.IS_RUNNING = True
        while self.IS_RUNNING:
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
            if self.SHOW:
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
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = abs(255-img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.IMAGE = cv2.addWeighted(img, self.CONTRAST, img, 0, self.BRIGHTNESS)
        return self.IMAGE


if __name__ == "__main__":
    picv = picv(start=True, show=True)
    while True:
            pass
