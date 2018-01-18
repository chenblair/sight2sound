# pythone 3
# Change these:
# The input file must be grayscale

import hilbert_curve as hc
from PIL import Image
import math
from time import sleep
import alsaaudio
import numpy as np
from threading import Thread, Semaphore

mutex = Sempahore(value=0)

signal_time_length = 1  # in seconds
sample_rate = 44100.0  # in Hz
# outAudio = None

# def playInfiniteAudio():
#   out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, 
#             device='default', 
#             mode=alsaaudio.PCM_NONBLOCK)
#   out.setchannels(1)
#   out.setrate(int(sample_rate))
#   out.setformat(alsaaudio.PCM_FORMAT_U32_BE)
#   out.setperiodsize(int(sample_rate)) #TODO this may be too big
#   count = 0
#   while True:
#     while outAudio is None:
#       print("Sleeping for eternity..." + str(count + 1))
#       count += 1
#       sleep(1)
# 
#     print("Playing...")
#     mutex.acquire()
#     assert(len(outAudio)==4*int(sample_rate*signal_time_length)) #TODO this will need to commented out when in production
#     out.write(outAudio)
#     mutex.release()
#     sleep(signal_time_length*5)
#     print("Played")

def setup_camera_taker():
  while True:
    sleep(1)
    mutex.release()

def main():
  input_file = '64x64.png'

  out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, 
            device='default', 
            mode=alsaaudio.PCM_NONBLOCK)
  out.setchannels(1)
  out.setrate(int(sample_rate))
  out.setformat(alsaaudio.PCM_FORMAT_U32_BE)
  out.setperiodsize(int(sample_rate)) #TODO this may be too big

  t = Thread(target=setup_camera_taker)
  t.start()

  lowest_frequency = 220  # In hz!
  highest_frequency = 8410
  frequency_step = 2

  def checkPowerOf2(num):
    return ((num & (num - 1)) == 0) and num != 0

  while True:
    mutex.acquire()
    img = Image.open(input_file).convert("L")
    pixels = img.load()

    x, y = img.size
    if ((x != y) or (checkPowerOf2(x) == False)):
      exit("The image has to be a power of 2.")

    #print("Serialising pixels...")
    output = [
        pixels[hc.d2xy(math.log(x * y, 2), i)]
        for i in range(x*x)
        ]

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
    outputAudio += 1  
    outputAudio *= 16384 * 2

    byte_data = outputAudio.astype('float32').tobytes()
    out.write(byte_data)
    

if __name__ == '__main__': main()
