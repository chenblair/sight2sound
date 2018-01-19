import numpy as np
sample_rate = 44100.0  # in Hz
signal_time_length = 1  # in seconds
T = 1 / sample_rate  # spacing between sample points
N = int(sample_rate * signal_time_length)  # number of sample points
fs = np.zeros(N//2 + 1)
fs[int(440*T*N)] = 1 / 255 * 500
signal = np.fft.irfft(fs)
fs2 = np.fft.rfft(signal)
np.argmax(np.abs(fs2))/(T*N)
#fs[int(440*T*N)] = 1 / 255 * output[i]