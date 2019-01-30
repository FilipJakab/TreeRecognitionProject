from os.path import isfile, isdir, join
import sys, json
from os import makedirs
from caffe2.python import workspace, core, caffe2_pb2
import numpy as np

from DataHelpers import SplitImages, CreateLmdb

from ModelHelpers import LoadPretrainedSqueezenetModel

from DatasetHelpers import LmdbDatasetWrapper

from Constants import (
	batchSize, 
	imageSquaredDimension,
	squeezenetFolder,
	trainLmdbPath,
	trainIters
)

def Confirm(message):
	return raw_input(message + ' [[y]/n] ') in ['y', 'Y', 'yes', '']

def RunValidation(model, i):
	print 'before val:'
	PrintStatistics(i)
	workspace.RunNet(model.net)
	print 'after val:'
	PrintStatistics(i)

def PrintStatistics(i):
	acc = workspace.FetchBlob('accuracy')
	loss = workspace.FetchBlob('loss')

	print '%04d: acc: %.4f; loss: %.4f;' % (i, acc, loss)

def EnsureFeatureLabelMap(baseImageLabelMapPath, imageLabelPath, ratio, alreadyLoaded=None):
	subSet, rest = SplitImages(baseImageLabelMapPath, ratio, alreadyLoaded)
	if not isfile(imageLabelPath):
		with open(imageLabelPath, 'w') as f:
			json.dump(subSet.tolist(), f, indent=2)

	return rest

def EnsureLmdb(
	lmdbPath,
	imageLabelMapPath,
	imageSquaredDimension):
	if not isdir(lmdbPath):
		makedirs(lmdbPath)
		CreateLmdb(
			lmdbPath,
			imageLabelMapPath,
			imageSquaredDimension
		)

def SqueezenetRetrain(labels):
	devOps = core.DeviceOption(caffe2_pb2.CUDA, 0)

	squeezenetModel = LoadPretrainedSqueezenetModel('squeezenet_model',
		trainLmdbPath, len(labels), batchSize, imageSquaredDimension,
		join(squeezenetFolder, 'init_net.pb'), join(squeezenetFolder, 'predict_net.pb'),
		devOps, len(labels), ['conv10_w', 'conv10_b'])

	datasetWrapper = LmdbDatasetWrapper(trainLmdbPath, batchSize, imageSquaredDimension)
	datasetWrapper.Open()

	# model init
	firstRow = datasetWrapper[0]
	workspace.FeedBlob('data', np.stack([firstRow[0]]), device_option=devOps)
	workspace.FeedBlob('label', np.stack([firstRow[1]]), device_option=devOps)
	workspace.RunNetOnce(squeezenetModel.param_init_net)
	workspace.CreateNet(squeezenetModel.net, overwrite=True)

	for epoch in range(trainIters):
		batch = datasetWrapper.GetBatch(epoch)
		workspace.FeedBlob('data', batch[0])
		workspace.FeedBlob('label', batch[1])
		workspace.RunNet(squeezenetModel.net)

		print 'acc: %.4f\t\tloss: %.4f' % (workspace.FetchBlob('accuracy'), workspace.FetchBlob('loss'))

	datasetWrapper.Close()
	del datasetWrapper
