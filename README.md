# Sight to Sound
This raspberry pi3 project programmed in Python3 tranforms image input to soundscapes. This hypothetically can help blind people perceive their surroundings. How does it work? Present in every clip of audio are different sound frequencies with different amplitudes. We then use a Hilbert curve to map this frequency domain (which is 1 dimension) to the 2 dimensional Image. So each pixel in the Image corresponds to a unique frequency. We then simply make the amplitude of the frequency correspond to the pixel intensity in greyscale. Watch a Youtube [video](https://www.youtube.com/watch?v=3s7h2MHQtxc) that explains the concepts better.

To run, simply run `python3 main.py`.

## Demo
<a href="http://www.youtube.com/watch?feature=player_embedded&v=1P_RSq-vCUA
" target="_blank"><img src="http://img.youtube.com/vi/1P_RSq-vCUA/0.jpg" 
alt="Youtube demo" width="240" height="180" border="10" /></a>

*Please excuse our poor videography! We filmed this in a one-take at the end of the hackathon, so we were very tired.*

## Dependencies
1. Software
   * python3
   * numpy (for `numpy.fft.irfft`)
   * alsaaudio
   * picamera
   * hilbert_curve (found [here](https://people.sc.fsu.edu/~jburkardt/py_src/hilbert_curve/))
   * PIL (python image library)
   * threading
2. Hardware
   * [Raspberry pi3](https://www.amazon.com/Raspberry-Pi-RASPBERRYPI3-MODB-1GB-Model-Motherboard/dp/B01CD5VC92)
   * [Raspberry Pi Camera](https://www.adafruit.com/product/3099)

## Caveats
The `hilbert_curve` library that we found produces hilbert curves in a fairly inefficient manner, so increasing the resolution from 64x64 to 2048x2048, for example, may run for an obscenely long time preparing the curve.

Also, for some unknown reason to us, the `write` function provided in alsaaudio normalizes (?) the amplitudes of the signal passed in, so when we used the function to write a sine curve with amplitude `1e-12`, it produced loud audio exactly the same as with amplitude `1e0`.

Finally, the algorithm plays .8 seconds (constant stored as `signal_time_length`) of audio for each image, and then after that .8 second period it will capture a new image. This creates a refresh period of around 1 second for the audio out. Theoretically, we should be able to change the `signal_time_length` to a smaller period, but there is something weird the python interpreter does with thread locks which prevents it from working.

## Team
+ [shguan10](https://github.com/shguan10/)
+ [17zhangw](https://github.com/17zhangw/)
+ [unbrace3](https://github.com/unbrace3/)
+ [ramvenkat98](https://github.com/ramvenkat98/)
+ [imjal](https://github.com/imjal/)

## Acknowledgements
We would like to acknowledge the following:
* Build18 officers and sponsers. [Build18](https://build18.herokuapp.com/) is the 4.5-day hackathon in which we completed this project. The hackathon provided us with funding for building materials, space for working, and snacks to keep us going.
* 3Blue1Brown (an awesome youtube channel that made a [great video](https://www.youtube.com/watch?v=3s7h2MHQtxc) on the Hilbert curve and its potential use in mapping visual space to audio space).
* minerscale for open-sourcing initial (if extremely inefficient) [code](https://github.com/minerscale/sight-as-sound).
* jburkardt for providing [hilbert curve code](https://people.sc.fsu.edu/~jburkardt/py_src/hilbert_curve/)
