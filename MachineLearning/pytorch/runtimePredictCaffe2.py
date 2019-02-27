'''
	loads pytorch model in onnx format and creates caffe2 predictor out of it
	then loads image from path in arg and runs model upon it
'''

import sys
from os.path import isfile
from os import walk
import numpy as np

import torch
from caffe2.python.onnx import backend
import onnx

from PIL import Image

from constants import (
	modelDeployParamsPath,
	productionTransformationFlow,
	dataDir
)

class Predictor:
	def __init__(self):
		print 'predictor created'
		onnxModel = onnx.load(modelDeployParamsPath)
		onnx.checker.check_model(onnxModel)
		self.predictor = backend.prepare(onnxModel)# , device='CUDA:0')
		del onnxModel
	def Run(self, imagePaths):
		preppedImages = []
		for imagePath in imagePaths:
			preppedImages.append(
				productionTransformationFlow(Image.open(imagePath))
					.data.numpy()
			)
		# prepedImage = prepedImage.to(device='cuda:0')
		batch = [np.stack(preppedImages, axis=0)]
		result = self.predictor.run(batch)
		del batch
		del preppedImages
		# return st batch
		return result[0]

# labels = walk(dataDir)[1]
