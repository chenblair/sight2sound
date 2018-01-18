from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (64, 64)
# camera.resolution = (2, 2)
camera.start_preview()
# Camera warm-up time
sleep(2)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

for filename in camera.capture_continuous('img{counter:03d}.png'):
   print('Captured %s' % filename)
    # sleep(10) # wait 5 minutes
# camera.capture_sequence(['image%02d.png' % i for i in range(10)])
