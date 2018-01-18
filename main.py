#! /usr/bin/env python

# I used python 3.6 with an Anaconda install on Linux to make this.
# If you don't use all of those, your mileage may vary.

# Change these:
# The input file must be grayscale

def main():
	input_file = 'testImage1.png'
	output_wav = 'testImage1.wav'

# Keep this number low.
# It takes ages to generate
#	num_seconds = 0.5

	lowest_frequency = 30 # In hz!
	highest_frequency = 8410
	frequency_step = 2

# A value that directly detirmines the frequency
# Find the highest frequency with this:
# 2**(255/frequency_n)*lowest_frequency
# That puts the max frequency at just under 2562hz
	#frequency_n = 72 # Not in hz!

# ===========================================================================

# This is a little library I found online so I didn't have to
# Make the hilbert curve stuff myself. A real time saver!
# hilber_curve.py is included in the zip.
	import hilbert_curve as hc
	from PIL import Image
	import math
	import wave
	import numpy as np

# Makes sine waves, this is what I'll be using for
# To make the individual frequencies
# f = frequency
# a = amplitude
# t = time
#	def generateSine(f,a,t):
#		return (math.sin(t/44100*2*math.pi*f)*a)

# Checks if the number is a power of 2.
	def checkPowerOf2(num):
		return ((num & (num - 1)) == 0) and num != 0

# Open the image
	img = Image.open(input_file).convert("L")
	pixels = img.load()

# Get the size of the image
	x,y = img.size
	print(x, y)
# It doesn't fit the criteria. Tish tish tish.
	if ((x != y) or (checkPowerOf2(x) == False)):
		exit("The image has to be a power of 2.")


	print ("Serialising pixels...")
# Here's where it gets interesting.
# We create the output list
	output = []
# Then, we iterate over every pixel.
	"""testImage0 = np.zeros((64, 64))
	testImage1 = np.zeros((64, 64))"""
	for i in range(0,x**2):
	# hc.d2xy() Turns a linear integer
	# into the x,y coordinates of a plane.
		hilbert = hc.d2xy(math.log(x*y,2),i)
		"""
		if i <20:
			testImage0[hilbert[0]][hilbert[1]] = 255
		elif i > 4075:
			testImage1[hilbert[0]][hilbert[1]] = 255
		"""
	# Use those coordinates to get the pixel value
	# And thus serialise a 2d plane.
		output.append(pixels[hilbert])
	"""
	print(testImage0)
	print(testImage1)
	testImage0 = Image.fromarray(np.uint8(testImage0) , 'L')
	testImage1 = Image.fromarray(np.uint8(testImage1) , 'L')
	testImage0.save("testImage0.png")
	testImage1.save("testImage1.png")
	testImage2 = np.zeros((64, 64))
	for i in range(0, 32):
		testImage2[i] = np.full((64), 255)
	print(testImage2)
	testImage2 = Image.fromarray(np.uint8(testImage2), 'L')
	testImage2.save("testImage2.png")
	
	testImage3 = np.full((64, 64), 255)
	print(testImage3)
	(x, y) = testImage3.shape
	print(x, y)
	for i in range(len(testImage3)):
		for j in range(len(testImage3[0])):
			assert(testImage3[i][j] == 255)
	testImage3 = Image.fromarray(np.uint8(testImage3), 'L')
	print(testImage3.size)
	testImage3.save("testImage3.png")
	"""

	print ("Generating audio...")
# Generate the Audio output list
#	outputAudio = [0]*(int(44100*num_seconds))

	#pixel_count = 0
# Iterate over every sing pixel in the list
	N = 44100.0#64.0 #number of points
	T = 1/N  #spacing between points

	myx = np.linspace(0, 2*np.pi*N*T, N)
	totalAmplitudesOverTime = np.zeros(int(N))
	frequency = lowest_frequency
	for pixel in output:
	# if pixel_count % 10 == 0:
		#print (pixel_count,"pixels completed out of", x*y, "          ", end="\r")
		#pixel_count += 1

	# I'm mapping the audio exponetially instead of linearly becase that's the way
	# The human ear works. That made the most sence to me.
	# The way I mapped those frequencies is arbitary, except that I tried to make it
	# so the frequencies were within the loudest part of human hearing ~ 220hz to 2561hz
		#frequency = 2**(pixelNo/frequency_n)*lowest_frequency
		totalAmplitudesOverTime += 1/255 * pixel * np.sin(frequency*2*np.pi*myx)
		frequency += 2
	#for t in range(0,len(outputAudio)):
		# Constantly layer the audio on top of one another until it's complete
		# We use a really big offset to t becuase if we don't we get a really weird tone that quickly
		# Tapers off. If you can figure out why this is I'll be really happy
		#outputAudio[t] += generateSine(frequency,1/(x*y/2),t+524288)
	outputAudio = totalAmplitudesOverTime
	print('\n:len of outputAudio :'+str(len(outputAudio)))
	print("Converting...")
# Do some conversion work. At the moment the audio is between -1 and 1
# I need to map -1 and 1 to 0 and 65536
	outputAudio += 1
	outputAudio *= 16384
#for i in range(0,len(outputAudio)):
	# Add one
	#outputAudio[i] += 1
	# Multiply by 16384, the reason why I'm not multiplying by the maximum amount
	# is because python wave uses singed not unsinged and to_bytes uses unsinged
	# so nobody wins and the volume gets slashed in half
	#outputAudio[i] = outputAudio[i] * 16384

	# Convert it to an integer so to_bytes doesn't throw a hissy fit (RIP)
	#outputAudio[i] = int(outputAudio[i])

	print("Writing file to disk, also converting the sound data to bytes.")

	#from scipy.io import wavfile

	#with open('output.wav','wb') as f:
	#	wavfile.write(f,int(1/T),outputAudio)

# Open the output file
	audio_output = wave.open(output_wav, 'wb')
# Set it to one channed 16bit 44100hz no compression
	audio_output.setparams((1, 4, 44100, 0, 'NONE', 'not compressed'))
	#audio_output.setparams((1,2,int(1/T),0,'NONE','not compressed'))

# Write the output to the file
	audio_output.writeframes(outputAudio.astype('float32').tobytes())
	#for i in outputAudio:
	#	audio_output.writeframes(i.to_bytes(2,'little'))


if __name__ == '__main__': main()
