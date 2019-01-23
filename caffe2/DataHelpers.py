import lmdb, glob, json
from os.path import isdir, join
import skimage
import numpy as np

# custom transforms
from DataTransforms import CropCenter, ResizeImage

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

def CreateLmdb(lmdbPath, imageListPath, image_size):
	imageList = None
	with open(imageListPath, 'r') as f:
		imageList = json.load(f)

	env = lmdb.open(lmdbPath, map_size=1<<35, create=True)
	with env.begin(write=True) as transaction:
		imageRootFolderPath = '/'.join(imageListPath.split('/')[:-1])
		count = 0
		for image in imageList:
			img = None
			try:
				# print 'processing image:', image
				img = skimage.io.imread(join(imageRootFolderPath, image[0])).astype(np.float)
				img = PreprocessImage(img, image_size)
			except ValueError:
				print 'image %s is not colorful, omitted' % image
				continue
			except IOError:
				print 'image %s is not readable, omitted' % image
				continue

			proto = caffe2_pb2.TensorProtos()
			# insert image to proto
			imageTensor = proto.protos.add()
			imageTensor.dims.extend(img.shape)
			imageTensor.data_type = 1
			imageTensor.float_data.extend(np.reshape(img, np.prod(img.shape)))

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
		
		print 'Finished creating lmdb. Rows inserted: {}'.format(count)

def SplitImages(allImagesJsonPath, ratio):
	allImages = None
	# load images table
	with open(allImagesJsonPath, 'r') as f:
		allImages = json.load(f)
	
	result = []
	for image in allImages.keys():
		result.append([image, allImages[image]])

	# shuffle images
	result = np.random.permutation(result)

	amount = int(ratio*len(result))
	train = result[:amount]
	val = result[amount:]

	return train, val

def FetchRowCount(lmdbPath):
	env = lmdb.open(lmdbPath)
	count = 0
	with env.begin() as txn:
		count = txn.stat()['entries']
	
	return count
