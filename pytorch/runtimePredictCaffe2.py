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

def Run(imagePath):
	onnxModel = onnx.load(modelDeployParamsPath)
	onnx.checker.check_model(onnxModel)
	predictor = backend.prepare(onnxModel, device='CUDA:0')

	prepedImage = productionTransformationFlow(Image.open(imagePath))
	prepedImage.cuda()

	result = predictor.run([prepedImage.data.numpy()[np.newaxis]])

	return result[0][0]

# labels = walk(dataDir)[1]
