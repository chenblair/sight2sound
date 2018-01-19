import pickle
def getOutput(pixels):
	with open("hc.dat","rb") as f: hc = pickle.load(f)
	return [pixels[hc]]
