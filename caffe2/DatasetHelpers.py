# inspired by https://nbviewer.jupyter.org/gist/kyamagu/6cff70840c10ca374e069a3a7eb00cb4/dogs-vs-cats.ipynb

from caffe2.python import caffe2_pb2
import numpy as np
import lmdb, json, skimage
from os.path import join

from DataHelpers import FetchRowCount, PreprocessImage
from DataTransforms import CropCenter# CalculateAugmentRatio

class LmdbDatasetWrapper(object):
	def __init__(self, lmdbPath, batchSize, imageSize, newImageSize=None):
		self.lmdbPath = lmdbPath
		self.Enviroment = lmdb.open(lmdbPath, readonly=True, create=False)
		self.Transaction = None
		self.Cursor = None
		self.BatchSize = batchSize
		self.ImageSize = imageSize
		self.NewImageSize = newImageSize

	def __len__(self):
		return FetchRowCount(self.lmdbPath)

	def __getitem__(self, index):
		if not self.Cursor.set_range(str(index)):
			raise IndexError('invalid index')
		_, imgTensorStr = self.Cursor.item()
		return self._prepareImage(imgTensorStr)

	def Open(self):
		if self.Transaction == None: 
			self.Transaction = self.Enviroment.begin(write=False)
			self._createCursor()

	def Close(self):
		self.Cursor = None
		self.Transaction = None

	def _parseStringProto(self, proto):
		rowProto = caffe2_pb2.TensorProtos()
		rowProto.ParseFromString(proto)
		imageArr = np.reshape(rowProto.protos[0].float_data, [3, self.ImageSize, self.ImageSize])
		label = int(rowProto.protos[1].int32_data[0])
		return imageArr, label

	def _createCursor(self):
		if self.Cursor != None:
			return

		self.Cursor = self.Transaction.cursor()

	def __del__(self):
		if self.Transaction != None:
			self.Transaction = None
		self.Enviroment.close()

	def _prepareImage(self, imageProtoStr):
		image, label = self._parseStringProto(imageProtoStr)

		if self.NewImageSize not in [None, self.ImageSize]:
			if self.NewImageSize == self.ImageSize:
				pass
			if self.NewImageSize > self.ImageSize:
				nImage = np.zeros((3, self.NewImageSize, self.NewImageSize)).astype(np.float32)
				startPos = (self.NewImageSize - self.ImageSize) / 2
				nImage[:, startPos:self.ImageSize + startPos, startPos:self.ImageSize + startPos] = image
				image = nImage
			else:
				image = CropCenter(image, self.NewImageSize)

		image = image - 0.5

		return image, label

	def GetBatch(self, batchIndex):
		data, labels = [], []
		self.Cursor.set_range(str(batchIndex * self.BatchSize))
		i = 0
		for item in self.Cursor:
			if i >= self.BatchSize:
				break
			image, label = self._prepareImage(item[1])
			data.append(image)
			labels.append(label)
			i += 1
		# for i in range(self.BatchSize):
		# 	result.append(self[(batchIndex * self.BatchSize) + i])
		return np.stack(data, axis=0).astype(np.float32), np.stack(labels, axis=0).astype(np.int32)

class DatasetOnTheFly(object):
	"""docstring for DatasetOnTheFly"""
	def __init__(self, imageMapPath, batchSize, imageSize):#, maxDeviation=0, deviationStep=8):
		with open(imageMapPath, 'r') as f:
			self.imageMap = json.load(f)
		self.baseDir = '/'.join(imageMapPath.split('/')[:-1])
		self.batchSize = batchSize
		self.imageSize = imageSize
		# self.augmentAmplifier = CalculateAugmentRatio(maxDeviation, deviationStep)
	def GetFirst(self):
		# print self.imageMap[0][0]
		img = skimage.io.imread(join(self.baseDir, self.imageMap[0][0]))
		return PreprocessImage(img, self.imageSize, True, True), self.imageMap[0][1]
	def GetBatch(self, batchIndex):
		# enable repeatable iterating over images
		if batchIndex + 1 > len(self.imageMap) / self.batchSize:
			batchIndex = batchIndex % (len(self.imageMap) / self.batchSize)

		data = []
		label = np.empty((self.batchSize,), dtype=np.int32)
		for i, imagePair in enumerate(self.imageMap[(self.batchSize*batchIndex):(self.batchSize*(batchIndex + 1))]):
			img = skimage.io.imread(join(self.baseDir, imagePair[0]))
			data.append(PreprocessImage(img, self.imageSize, True, True))
			label[i] = int(imagePair[1])
		return np.stack(data).astype(np.float32), np.stack(label).astype(np.int32)
