def main():
	from scipy.io import wavfile as wav
	import numpy as np
	filename = "testQuad4.png1e-100.wav"
	rate,data=wav.read(filename)
	w=np.abs(np.fft.rfft(data))
	with open(filename+".Freqs.txt","w") as f:
		for i in range(len(w)):
			f.write(str(w[i]))
			f.write("\n")

if __name__ =='__main__': main()