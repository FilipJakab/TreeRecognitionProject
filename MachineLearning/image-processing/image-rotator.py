'''
	Rotates images in specified dir (arg) by 90 degs N times where N is specified in arg
'''

import numpy as np
from os import listdir
from os.path import join
import sys, skimage.io

if len(sys.argv) < 3:
	print 'insufficent amount of params'
	sys.exit(1)

for img in listdir(sys.argv[1]):
	path = join(sys.argv[1], img)
	print 'processing %s' % path
	image = skimage.io.imread(path)
	image = np.rot90(image, int(sys.argv[2]))
	skimage.io.imsave(path, image)

sys.exit(0)
