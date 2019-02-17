import numpy as np

def SoftmaxFn(input):
	e = np.exp(input)
	return e / np.sum(e)
