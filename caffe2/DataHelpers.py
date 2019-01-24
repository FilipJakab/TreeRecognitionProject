import lmdb, glob, json
from os.path import isdir, join
import skimage
import numpy as np

# custom transforms
from DataTransforms import CropCenter, ResizeImage, AugmentImage

# caffe2 stuff
from caffe2.python.core import caffe2_pb2

def PreprocessImage(img, imageDimension, castImage=False, scaleImage=False):
	if len(img.shape) != 3:
		raise ValueError()
	# resize
	img = ResizeImage(img, imageDimension)
	# crop center
	img = CropCenter(img, imageDimension)
	# convert from RGB to BGR
	img = img[:, :, (2, 1, 0)]
	# convert from HWC to CHW
	img = np.transpose(img, (2, 0, 1))
	# convert to float
	if castImage:
		img = img.astype(np.float32)
	# convert to range from 0-255 to 0 - 1
	if scaleImage:
		img *= (1. / 256)
	
	return img

def CreateLmdb(lmdbPath, imageListPath, imageSize, batchSize=1500):
	imageList = None
	with open(imageListPath, 'r') as f:
		imageList = json.load(f)

	count = 0
	env = lmdb.open(lmdbPath, map_size=1<<35, create=True)

	augmentAmplifier = (4 * (((64 / 32) + 1) ** 2))
	computedBatchSize = batchSize / augmentAmplifier
	for batch in [imageList[x:x+computedBatchSize] for x in range(0, len(imageList), computedBatchSize)]:
		print 'Starting new batch..'
		with env.begin(write=True) as transaction:
			imageRootFolderPath = '/'.join(imageListPath.split('/')[:-1])
			for image in batch:
				img = None
				try:
					# print 'processing image:', image
					img = skimage.io.imread(join(imageRootFolderPath, image[0])).astype(np.uint8)
				except ValueError:
					print 'image %s is not colorful, omitted' % image
					continue
				except IOError:
					print 'image %s is not readable, omitted' % image
					continue

				for augmented in AugmentImage(img, maxDeviation=64, deviationStep=32):
					augmented = PreprocessImage(augmented, imageSize)

					proto = caffe2_pb2.TensorProtos()
					# insert image to proto
					imageTensor = proto.protos.add()
					imageTensor.dims.extend(augmented.shape)
					imageTensor.data_type = 1
					imageTensor.float_data.extend(np.reshape(augmented, np.prod(augmented.shape)))

					# insert label to proto
					labelTensor = proto.protos.add()
					labelTensor.data_type = 2
					labelTensor.int32_data.append(int(image[1]))

					# insert proto to lmdb
					transaction.put(
						'{}'.format(count),
						proto.SerializeToString()
					)

					count = count + 1
					if (count % 100) == 0:
						print 'inserted {} rows..'.format(count)
		print 'Inserted %d images out of %d' % (count, len(imageList) * augmentAmplifier)
	print 'Finished creating lmdb. Rows inserted: {}'.format(count)

def SplitImages(allImagesJsonPath, ratio, valRatio):
	if ratio + valRatio >= 1:
		raise ValueError('rations does not make sense')

	allImages = None
	# load images table
	with open(allImagesJsonPath, 'r') as f:
		allImages = json.load(f)
	
	result = []
	for image in allImages.keys():
		result.append([image, allImages[image]])

	# shuffle images
	result = np.random.permutation(result)

	amount = len(result)
	trainTestLimit = int(ratio*amount)
	trainValLimit = int(valRatio*amount)
	
	train = result[:trainTestLimit]
	test = result[trainTestLimit:-trainValLimit]
	val = train[-trainValLimit:]

	return train, test, val

def FetchRowCount(lmdbPath):
	env = lmdb.open(lmdbPath)
	count = 0
	with env.begin() as txn:
		count = txn.stat()['entries']
	
	return count
