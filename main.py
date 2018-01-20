# python 3

# The input file must be grayscale

import hilbert_curve as hc
from PIL import Image
import math
from time import sleep
import alsaaudio
from picamera import PiCamera
import numpy as np
from threading import Thread, Semaphore

#==========================================
#CONSTANTS
signal_time_length = 0.8  # in seconds
sample_rate = 44100.0  # in Hz

lowest_frequency = 50  # In hz!
highest_frequency = 20000 #8410
frequency_step = (highest_frequency - lowest_frequency)/(res1*res1)

res1 = 64
res2 = 64
#==========================================

mutex = Semaphore(value=0)
cameraSem = Semaphore(value=1)

def isPowOf2(num):
  return ((num & (num - 1)) == 0) and num != 0

if ((res1 != res2) or not isPowOf2(res1)):
  exit("The image has to be a power of 2.")

gPic = None

def setup_camera_taker():
  camera = PiCamera()
  camera.resolution = (res1, res2)
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
    cameraSem.acquire()
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
    #sleep(0.7) #TODO TWEAK THIS TO MAKE IT A CONTINUOUS STREAM OF AUDIO

def main():
  # BEGIN SETTING UP AUDIO OUT
  out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, 
            device='default', 
            mode=alsaaudio.PCM_NONBLOCK)
  out.setchannels(1)
  out.setrate(int(sample_rate))
  out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
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

  while True:
    mutex.acquire()
    
    output = [gPic[curve[i][0]][curve[i][1]] for i in range(res1*res1)]
    
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

    #print("Converting...")
    outputAudio *=1e-100

    byte_data = outputAudio.astype('float16').tobytes()
    out.write(byte_data)
    cameraSem.release()

    """
    import wave
    with open(input_file+"1e-100.wav","wb") as f:
      wavout = wave.open(f,'wb')
      wavout.setparams((1,2,44100,0,'NONE','not compressed'))
      wavout.writeframes(byte_data)
    print("sleeping")
    sleep(20)
    """
    

if __name__ == '__main__': main()
