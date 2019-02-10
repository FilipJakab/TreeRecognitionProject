import lmdb, glob, json
from os.path import isdir, join
from os import listdir
from sys import getsizeof as getSize
import skimage
import numpy as np
from PIL import Image

import pandas as pd

# caffe2 stuff
from caffe2.python.core import caffe2_pb2

# custom transforms
from DataTransforms import CropCenter, ResizeImage, AugmentImage, CalculateAugmentRatio

def PreprocessImage(img, imageDimension, castImage=False, scaleImage=False):
	if len(img.shape) != 3:
		raise ValueError()
	# resize
	if not (imageDimension in img.shape):
		img = ResizeImage(img, imageDimension)
	# crop center
	if img.shape[0] != imageDimension or img.shape[1] != imageDimension:
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
		img *= (1. / 255)
	
	return img

def EnsureLmdb(lmdbPath, imageListPath, imageSize, insertBatchSize=1500):
	imageList = None
	with open(imageListPath, 'r') as f:
		imageList = json.load(f)
	
	augmentAmplifier = CalculateAugmentRatio(maxDeviation=64, deviationStep=16)

	env = lmdb.open(lmdbPath)

	env.set_mapsize(1<<40)

	count = FetchRowCount(env=env)
	computedBatchSize = insertBatchSize / augmentAmplifier

	if count == len(imageList) * augmentAmplifier:
		print 'Dataset is already filled..'
		return

	startFrom = count / augmentAmplifier

	for batch in [imageList[x:x+computedBatchSize-1] for x in range(startFrom, len(imageList), computedBatchSize)]:
		print 'Starting new batch..'
		with env.begin(write=True) as txn:
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

				for augmented in AugmentImage(img, maxDeviation=64, deviationStep=16, brightnessIndex=32):
					augmented = PreprocessImage(augmented, imageSize, scaleImage=True, castImage=True)

					InsertImageToLmdb(txn, count, augmented, int(image[1]))

					count = count + 1
					if (count % 1000) == 0:
						print 'inserted {} rows..'.format(count)
		print 'Inserted %d images out of %d' % (count, len(imageList) * augmentAmplifier)
	print 'Finished creating lmdb. Rows inserted: {}'.format(count)

def SplitImages(allImagesJsonPath, ratio, loadedImages=None):
	# load images
	if type(loadedImages) == type(None):
		with open(allImagesJsonPath, 'r') as f:
			allImages = json.load(f)
	else:
		allImages = loadedImages

	# shuffle images
	np.random.shuffle(allImages)

	subSetBorder = int(len(allImages) * ratio)

	return allImages[:subSetBorder], allImages[subSetBorder:]

def FetchRowCount(lmdbPath=None, env=None, txn=None):
	if txn != None:
		return txn.stat()['entries']
	
	if env == None and lmdbPath != None:
		env = lmdb.open(lmdbPath)
	elif env == None and lmdbPath == None:
		print 'lmdb path was not specified..'
		raise ValueError()
	with env.begin() as txn:
		count = txn.stat()['entries']
	
	return count

def InsertImageToLmdb(txn, key, img, label):
	proto = caffe2_pb2.TensorProtos()
	# insert image to proto
	imageTensor = proto.protos.add()
	imageTensor.dims.extend(img.shape)
	imageTensor.data_type = 1
	imageTensor.float_data.extend(img.flatten())

	# insert label to proto
	labelTensor = proto.protos.add()
	labelTensor.data_type = 2
	labelTensor.int32_data.append(label)

	# insert proto to lmdb
	txn.put(
		'{}'.format(key),
		proto.SerializeToString()
	)

def Cifar10ToLmdb(lmdbPath, cifar10Path, labelsFileName):
	trainImagesFolder = join(cifar10Path, 'train')
	
	idslabels = pd.read_csv(join(cifar10Path, labelsFileName), dtype={'id': np.int32, 'label': str})

	env = lmdb.open(lmdbPath, map_size=1<<25)

	with env.begin(write=True) as txn:
		for i, fileName in enumerate([join(trainImagesFolder, img) for img in listdir(trainImagesFolder)]):
			imageTensor = skimage.io.imread(fileName).astype(np.uint8)
			imageTensor = PreprocessImage(imageTensor, 32, True, True)

			proto = caffe2_pb2.TensorProtos()
			imgTensorProto = proto.protos.add()
			imgTensorProto.data_type = 1
			imgTensorProto.data_dims.extend(imageTensor.shape)
			imgTensorProto.float_data.extend(imageTensor.flatten())
