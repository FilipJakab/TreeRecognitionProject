'''
	loads pytorch model in onnx format and creates caffe2 predictor out of it
	then loads image from path in arg and runs model upon it
'''

import sys
from os.path import isfile
import numpy as np

from caffe2.python.onnx import backend
import onnx

from PIL import Image

from constants import (
	modelDeployParamsPath,
	deployTransformationFlow
)

if len(sys.argv) != 2 or not isfile(sys.argv[1]):
	print 'file "%s" could not be found..' % sys.argv[1]
	sys.exit(1)

onnxModel = onnx.load(modelDeployParamsPath)
onnx.checker.check_model(onnxModel)

pred = backend.prepare(onnxModel, device='CUDA:0')

prepedImage = deployTransformationFlow(Image.open(sys.argv[1]))

pred.run(np.array(prepedImage, dtype=np.float32))
