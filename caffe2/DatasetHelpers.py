# inspired by https://nbviewer.jupyter.org/gist/kyamagu/6cff70840c10ca374e069a3a7eb00cb4/dogs-vs-cats.ipynb

from caffe2.python import caffe2_pb2
import numpy as np
import lmdb

from DataHelpers import FetchRowCount

class LmdbDatasetWrapper(object):
	def __init__(self, lmdbPath, batchSize, imageSize):
		self.lmdbPath = lmdbPath
		self.Enviroment = lmdb.open(lmdbPath, readonly=True, create=False)
		self.Transaction = None
		self.Cursor = None
		self.BatchSize = batchSize
		self.ImageSize = imageSize
		pass
	def __len__(self):
		return FetchRowCount(self.lmdbPath)

	def __getitem__(self, index):
		if not self.Cursor.set_range(str(index)):
			raise IndexError('invalid index')
		_, imgTensorStr = self.Cursor.item()
		return self._parseStringProto(imgTensorStr)

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

	def GetBatch(self, batchIndex):
		data, labels = [], []
		self.Cursor.set_range(str(batchIndex * self.BatchSize))
		i = 0
		for item in self.Cursor:
			if i >= self.BatchSize:
				break
			image, label = self._parseStringProto(item[1])
			data.append(image)
			labels.append(label)
			i += 1
		# for i in range(self.BatchSize):
		# 	result.append(self[(batchIndex * self.BatchSize) + i])
		return np.stack(data).astype(np.float32), np.stack(labels).astype(np.int32)
