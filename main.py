# pythone 3

# The input file must be grayscale

import hilbert_curve as hc
from PIL import Image
import math
from time import sleep
import alsaaudio
from picamera import PiCamera
import numpy as np
from threading import Thread, Semaphore

mutex = Semaphore(value=0)

signal_time_length = 1  # in seconds
sample_rate = 44100.0  # in Hz
"""
 outAudio = None

 def playInfiniteAudio():
   out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, 
             device='default', 
             mode=alsaaudio.PCM_NONBLOCK)
   out.setchannels(1)
   out.setrate(int(sample_rate))
   out.setformat(alsaaudio.PCM_FORMAT_U32_BE)
   out.setperiodsize(int(sample_rate)) #TODO this may be too big
   count = 0
   while True:
     while outAudio is None:
       print("Sleeping for eternity..." + str(count + 1))
       count += 1
       sleep(1)
 
     print("Playing...")
     mutex.acquire()
     assert(len(outAudio)==4*int(sample_rate*signal_time_length)) #TODO this will need to commented out when in production
     out.write(outAudio)
     mutex.release()
     sleep(signal_time_length*5)
     print("Played")
"""

def isPowOf2(num):
  return ((num & (num - 1)) == 0) and num != 0

def setup_camera_taker():
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
  
  while True:
    mutex.release()
    sleep(1)

def main():
  input_file = '64x64.png'

  # BEGIN SETTING UP AUDIO OUT
  out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, 
            device='default', 
            mode=alsaaudio.PCM_NONBLOCK)
  out.setchannels(1)
  out.setrate(int(sample_rate))
  out.setformat(alsaaudio.PCM_FORMAT_U32_BE)
  out.setperiodsize(int(sample_rate)) #TODO this may be too big
  # END SETTING UP AUDIO OUT

  t = Thread(target=setup_camera_taker)
  t.start()

  # BEGIN SETTING UP HILBERT CURVE
  sizex = 64
  sizey = 64 #TODO make this dependent on the camera taken pics
  curve = [ # curve is list of tuples along hc
    hc.d2xy(math.log(sizex * sizey, 2), i) 
    for i in range(sizex*sizex)
  ]
  # END SETTING UP HILBERT CURVE

  lowest_frequency = 220  # In hz!
  highest_frequency = 8410
  frequency_step = 2

  while True:
    mutex.acquire()
    
    #TODO we shouldn't have to load an image file, just take it directly from camera
    img = Image.open(input_file).convert("L")
    pixels = img.load()
    x, y = img.size
    if ((x != y) or not isPowOf2(x)):
      exit("The image has to be a power of 2.")

    #print("Serialising pixels...")
    output = [pixels[curve[i]] for i in range(x*x)]
    """
    output = [ 
        pixels[hc.d2xy(math.log(x * y, 2), i)]
        for i in range(x*x)
        ]
    """
    #print("Generating audio...")
    T = 1 / sample_rate  # spacing between sample points
    N = int(sample_rate * signal_time_length)  # number of sample points

    ### BEGIN IRFFT ROUTINE
    fs = np.zeros(N//2 + 1)
    frequency = lowest_frequency
    for i in range(len(output)):
      fs[int(frequency*T*N)] = 1 / 255 * output[i] #this will be the amplitude for this frequency
      frequency += frequency_step

    outputAudio = np.fft.irfft(fs)
    ### END IRFFT ROUTINE

    #print('\n:len of outputAudio :' + str(len(outputAudio)))
    #print("Converting...")

    # TODO because the amplitudes of the sines are proportional to the pixel intensity, the output is not necessarily between [-1,+1]
    print(np.ndarray.max(outputAudio))
    print(np.ndarray.min(outputAudio))
    diff = np.ndarray.max(outputAudio) - np.ndarray.min(outputAudio)
    scale = 65536 / diff
    outputAudio -= np.ndarray.min(outputAudio)
    outputAudio *= scale
    """
    outputAudio += 1  
    outputAudio *= 16384 * 2
    """
    byte_data = outputAudio.astype('float32').tobytes()
    out.write(byte_data)

if __name__ == '__main__': main()