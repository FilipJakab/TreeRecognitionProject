from os.path import isdir, isfile, join, exists, expanduser
from os import makedirs
import json, sys
import numpy as np

from PIL import Image

from caffe2.python import workspace, net_drawer, caffe2_pb2, core
from DataHelpers import CreateLmdb, FetchRowCount, SplitImages
from ModelHelpers import (
	CreateModel,
	CreateDeployModel,
	RunModel,
	InitModel,
	SaveModel,
	LoadTrainModel
)
from Constants import (
	imageSquaredDimension,
	batchSize,
	learningRate,
	trainLmdbPath,
	testLmdbPath,
	checkpointPath,
	labelsPath,
	imageLabelMapPath,
	trainImageLabelMapPath,
	testImageLabelMapPath,
	trainIters,
	statisticsEvery,
	workspaceRootFolder,
	initNetPath,
	predictNetPath
)

from Methods import (
	Confirm,
	RunValidation,
	PrintStatistics,
	EnsureFeatureLabelMap,
	EnsureLmdb,
	SqueezenetRetrain
)

from DatasetHelpers import LmdbDatasetWrapper

# check image_label_maps
rest = EnsureFeatureLabelMap(imageLabelMapPath, trainImageLabelMapPath, 0.7)
rest = EnsureFeatureLabelMap(imageLabelMapPath, trainImageLabelMapPath, 0.666, rest)
EnsureFeatureLabelMap(imageLabelMapPath, testImageLabelMapPath, rest, 1)

EnsureLmdb(trainLmdbPath, trainImageLabelMapPath, imageSquaredDimension)
EnsureLmdb(testLmdbPath, testImageLabelMapPath, imageSquaredDimension)

workspace.ResetWorkspace(workspaceRootFolder)

labels = None
print 'loading labels'
with open(labelsPath, 'r') as f:
	labels = json.load(f)

# load squeezenet and run it (not working)
# SqueezenetRetrain(labels)
# sys.exit(0)

if exists(initNetPath) and Confirm('pretrained model file found. load?'):
	trainModel = LoadTrainModel('train_model',
		trainLmdbPath, len(labels), batchSize,
		imageSquaredDimension, initNetPath
	)
	print 'train model loaded'
else:
	print 'models initialization'
	trainModel = CreateModel(
		'train_model',
		len(labels),
		imageSquaredDimension,
		trainLmdbPath,
		batchSize,
		learningRate=learningRate,
		scaffoldAccuracy=True
	)

print '---'
testModel = CreateModel(
	'test_model',
	len(labels),
	imageSquaredDimension,
	testLmdbPath,
	1,
	initParams=False,
	scaffoldAccuracy=True
)

print '---'

deployModel = CreateDeployModel(
	'deploy_model',
	'data',
	len(labels),
	imageSquaredDimension
)

print 'starting training of %d iterations' % trainIters

acc, loss, iterList = RunModel(
	trainModel,
	trainIters,
	statisticsEvery,
	statisticsHandler=PrintStatistics,
	)

testLen = FetchRowCount(testLmdbPath)
print 'starting testing of %d' % testLen
RunModel(testModel, testLen, 10, PrintStatistics)

if not Confirm('do y want to save model?'):
	print 'not saving model..'
	sys.exit(0)

SaveModel(workspace, deployModel, initNetPath, predictNetPath)

print 'done!'
