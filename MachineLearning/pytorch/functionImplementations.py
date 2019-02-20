import numpy as np

def SoftmaxFn(inputs):
	res = []
	for input in inputs:
		e = np.exp(input)
		res.append(e / np.sum(e))
	return res
