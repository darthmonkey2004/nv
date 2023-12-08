from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (1280, 720)
camera.vflip = True
camera.contrast = 10
camera.image_effect = "watercolor"
time.sleep(2)

camera.capture("/home/pi/Pictures/img.jpg")
print("Done.")