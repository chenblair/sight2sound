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

signal_time_length = .2  # in seconds
sample_rate = 44100.0  # in Hz

res1 = 64
res2 = 64

def isPowOf2(num):
  return ((num & (num - 1)) == 0) and num != 0

if ((res1 != res2) or not isPowOf2(res1)):
  exit("The image has to be a power of 2.")

gPic = None

def setup_camera_taker():
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
  
  while True:
    rgbPic = np.empty((res1 * res1 * 3,), dtype=np.uint8)
    #print("before capture")
    camera.capture(rgbPic, 'rgb')
    #print("after capture")
    rgbPic = rgbPic.reshape((res1, res1, 3))
    #print("here")

    global gPic
    gPic = [[
      (0.3 * rgbPic[i][j][0]) + (0.59 * rgbPic[i][j][1]) + (0.11 * rgbPic[i][j][2])
      for j in range(res2)
    ] for i in range(res1)]
    mutex.release()
    #sleep(0) #TODO TWEAK THIS

def main():
  #input_file = '64x64.png'

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
  print("starts hilbert_curve")
  q = math.log(res1 * res1, 2)
  curve = [ # curve is list of tuples along hc
    hc.d2xy(q, i) 
    for i in range(res1 * res1)
  ]
  print("done hilbert_curve")
  # END SETTING UP HILBERT CURVE

  lowest_frequency = 50  # In hz!
  highest_frequency = 8410
  frequency_step = (highest_frequency - lowest_frequency)/(res1*res1)

  while True:
    #print("here2")
    mutex.acquire()
    """
    #TODO we shouldn't have to load an image file, just take it directly from camera
    img = Image.open(input_file).convert("L")
    pixels = img.load()
    x, y = img.size
    """
    #print("Serialising pixels...")
    #output = [pixels[curve[i]] for i in range(x*x)]
    #def f(pvalue): return 0 if pvalue < 128 else 255
    def f(p): return p
    #print("here3")
    output = [gPic[curve[i][0]][curve[i][1]] for i in range(res1*res1)]
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
      fs[int(frequency*T*N)] = output[i] #this will be the amplitude for this frequency
      frequency += frequency_step

    outputAudio = np.fft.irfft(fs)
    ### END IRFFT ROUTINE

    #print('\n:len of outputAudio :' + str(len(outputAudio)))
    #print("Converting...")

    # TODO because the amplitudes of the sines are proportional to the pixel intensity, the output is not necessarily between [-1,+1]
    print(np.ndarray.max(outputAudio))#TODO debug remove this
    print(np.ndarray.min(outputAudio))
    #diff = np.ndarray.max(outputAudio) - np.ndarray.min(outputAudio)
    #scale = 65536 / diff
    outputAudio -= np.ndarray.min(outputAudio)
    outputAudio *= 1310.72
    """
    outputAudio += 1  
    outputAudio *= 16384 * 2
    """
    
    byte_data = outputAudio.astype('float32').tobytes()
    out.write(byte_data)

if __name__ == '__main__': main()