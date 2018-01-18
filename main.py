#! /usr/bin/env python

# I used python 3.6 with an Anaconda install on Linux to make this.
# If you don't use all of those, your mileage may vary.

# Change these:
# The input file must be grayscale

import hilbert_curve as hc
from PIL import Image
import math
from time import sleep
import alsaaudio
import numpy as np
from threading import Thread, Lock

mutex = Lock()

outAudio = []
def playInfiniteAudio():
        out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, device='default')
        out.setchannels(1)
        out.setrate(44100)
        out.setformat(alsaaudio.PCM_FORMAT_U32_BE)
        out.setperiodsize(1)
        count = 0
        while True:
                while len(outAudio) == 0:
                        print("Sleeping for eternity..." + str(count + 1))
                        count += 1
                        sleep(1)
                
                mutex.acquire()
                out.write(outAudio.astype('float32').tobytes())
                mutex.release()
                print("Playing for eternity...")


def main():
        input_file = '64x64.png'
        output_wav = 'output.wav'

        t = Thread(target=playInfiniteAudio)
        t.start()

        lowest_frequency = 220 # In hz!
        highest_frequency = 8410
        frequency_step = 2

        def checkPowerOf2(num):
                return ((num & (num - 1)) == 0) and num != 0

        while True:
                img = Image.open(input_file).convert("L")
                pixels = img.load()

                x,y = img.size
                if ((x != y) or (checkPowerOf2(x) == False)):
                        exit("The image has to be a power of 2.")

                print ("Serialising pixels...")
                output = []
                for i in range(0,x**2):
                        hilbert = hc.d2xy(math.log(x*y,2),i)
                        output.append(pixels[hilbert])

                print ("Generating audio...")
                N = 44100.0#64.0 #number of points
                T = 1/N  #spacing between points

                myx = np.linspace(0, 2*np.pi*N*T, N)
                totalAmplitudesOverTime = np.zeros(int(N))
                frequency = lowest_frequency

                for pixel in output:
                        totalAmplitudesOverTime += 1/255 * output[i] * np.sin(frequency*2*np.pi*myx)
                        frequency += 2
                
                outputAudio = totalAmplitudesOverTime
                print('\n:len of outputAudio :'+str(len(outputAudio)))
                print("Converting...")
        
                outputAudio += 1
                outputAudio *= 16384*2

                mutex.acquire()
                global outAudio
                outAudio = outputAudio
                mutex.release()


if __name__ == '__main__': main()
