from time import sleep
from picamera import PiCamera
import numpy as np

int res1 = 64;
int res2 = 64;

camera = PiCamera()
camera.resolution = (res1, res2)
# camera.resolution = (2, 2)
camera.start_preview()
# Camera warm-up time
sleep(2)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

rgbPic = np.empty((res1 * res1 * 3,), dtype=np.uint8)
gPic = np.empty((res1 * res1,), dtype=np.uint8)
gPic = gPic.reshape((res1, res2))

while true:
  camera.capture(rgbPic, 'rgb')
  rgbPic = rgbPic.reshape((res1, res2, 3))
  for i in range(res1):
    for j in range(res2):
      gPic[i][j] = (rgbPic[i][j][0] + rgbPic[i][j][1] + rgbPic[i][j][2]) / 3
  print('Captured')
    # sleep(10) # wait 5 minutes
# camera.capture_sequence(['image%02d.png' % i for i in range(10)])
