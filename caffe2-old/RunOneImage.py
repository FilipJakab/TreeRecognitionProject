from caffe2.python import workspace
from os.path import isfile, splitext
import sys, skimage, numpy as np
import operator

from ModelHelpers import LoadPredictor
from DataHelpers import PreprocessImage
from Constants import (
	imageSquaredDimension,
	initNetPath,
	predictNetPath
)

if not isfile(initNetPath) or not isfile(predictNetPath):
	print 'protobuf files were not found..'
	sys.exit(1)

if len(sys.argv) == 1:
	img = raw_input('image path: ')
else:
	img = sys.argv[1]

if (not isfile(img)) or (not splitext(img)[1] in ['.jpg', '.jpeg', '.JPG']):
	print 'image path does not exist or is not supported (only .jpg\'s)'
	sys.exit(1)

print 'loading predictor.. (%s, %s)' % (initNetPath, predictNetPath)

p = LoadPredictor(workspace, initNetPath, predictNetPath)

print 'predictor loaded.\npreprocessing image %s..' % img
img = skimage.io.imread(img)
img = PreprocessImage(img, imageSquaredDimension, castImage=True, scaleImage=True)
img = img[np.newaxis, :, :]

print "image preprocessed.\nguessing the image's content.."

probs = np.squeeze(np.asarray(p.run({
	'data': img
})))

print 'probabilities: '
print probs


print 'done!'
