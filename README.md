# Sight to Sound
This raspberry pi project programmed in Python3 tranforms image input to soundscapes. This hypothetically can help blind people perceive their surroundings. How does it work? Present in every clip of audio are different sound frequencies with different amplitudes. We then use a Hilbert curve to map this frequency domain (which is 1 dimension) to the 2 dimensional Image. So each pixel in the Image corresponds to a unique frequency. We then simply make the amplitude of the frequency correspond to the pixel intensity in greyscale. 

To run, simply run `python3 main.py`

## Dependencies
* python3
* numpy (for `numpy.fft.irfft`)
* alsaaudio
* picamera
* hilbert_curve (custom code for producing hilbert curve)
* PIL (python image library)
* threading

## Caveats
The hilbert curve library that we found produces hilbert curves in a fairly inefficient manner, so increasing the resolution from 64x64 to 2048x2048, for example, may run for an obscenely long time preparing the curve.

Also, for some unknown reason to us, the write function provided in alsaaudio normalizes (?) the amplitudes of the signal passed in, so when we used the function to write a sine curve with amplitude 1e-12, it produced loud audio exactly the same as with amplitude 1e0.

Finally, the algorithm plays .8 seconds (constant stored as `signal_time_length`) of audio for each image, and then after that .8 second period it will capture a new image. This creates a refresh period of around 1 second for the audio out. Theoretically, we should be able to change the `signal_time_length` to a smaller period, but there is something weird the python interpreter does with thread locks which does not make it work.

## Team
+ shguan10
+ 17zhangw
+ unbrace3
+ ramvenkat98
+ imjal

## Acknowledgements
We would like to acknowledge the following sources:
* 3Brown1Blue (an awesome youtube channel that made a [great video](https://www.youtube.com/watch?v=3s7h2MHQtxc) on the Hilbert curve and its potential use in mapping visual space to audio space).
* Build18 board and sponsers. [Build18](https://build18.herokuapp.com/) is the 4.5-day hackathon in which we completed this project. The hackathon provided us with funding for building materials, space for working, and snacks to keep us going.
* minerscale for open-sourcing initial (if extremely inefficient) [code](https://github.com/minerscale/sight-as-sound).
