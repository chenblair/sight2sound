from time import sleep
from picamera import PiCamera
import numpy as np

res1 = 64;
res2 = 64;

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

""""""
gPic = np.empty((res1 * res1,), dtype=np.uint8)
gPic = gPic.reshape((res1, res2))
""""""

while True:
  rgbPic = np.empty((res1 * res1 * 3,), dtype=np.uint8)
  camera.capture(rgbPic, 'rgb')
  rgbPic = rgbPic.reshape((res1, res2, 3))
  """"""
  for i in range(res1):
    for j in range(res2):
      gPic[i][j] = (0.3 * rgbPic[i][j][0]) + (0.59 * rgbPic[i][j][1]) + (0.11 * rgbPic[i][j][2])
  """
  gPic = [[
    (0.3 * rgbPic[i][j][0]) + (0.59 * rgbPic[i][j][1]) + (0.11 * rgbPic[i][j][2])
    for j in range(res2)
  ] for i in range(res1)]
  """
  print('Captured')
    # sleep(10) # wait 5 minutes
# camera.capture_sequence(['image%02d.png' % i for i in range(10)])
