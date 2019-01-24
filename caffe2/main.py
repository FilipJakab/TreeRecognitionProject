from os.path import isdir, isfile, join, exists
from os import makedirs
import json, sys

from PIL import Image

from caffe2.python import workspace
from caffe2.python import net_drawer
from DataHelpers import CreateLmdb, FetchRowCount, SplitImages
from ModelHelpers import (
	InitTrainModel,
	InitNonTrainingModel,
	InitDeployModel,
	RunModel,
	SaveModel,
	LoadTrainModel
)
from Constants import (
	imageSquaredDimension,
	batchSize,
	learningRate,
	trainLmdbPath,
	testLmdbPath,
	valLmdbPath,
	checkpointPath,
	labelsPath,
	imageLabelMapPath,
	trainImageLabelMapPath,
	testImageLabelMapPath,
	valImageLabelMapPath,
	trainIters,
	statisticsEvery,
	workspaceRootFolder,
	initNetPath,
	predictNetPath
)

from methods import Confirm, RunValidation, PrintStatistics

# check image_label_maps
if not (isfile(trainImageLabelMapPath) and isfile(testImageLabelMapPath) and isfile(valImageLabelMapPath)):
	try:
		train, test, val = SplitImages(imageLabelMapPath, 0.7, 0.1)
	except ValueError as err:
		print err
		sys.exit(1)
	with open(trainImageLabelMapPath, 'w') as f:
		json.dump(train.tolist(), f, indent=2)
	with open(testImageLabelMapPath, 'w') as f:
		json.dump(test.tolist(), f, indent=2)
	with open(valImageLabelMapPath, 'w') as f:
		json.dump(val.tolist(), f, indent=2)

# create val lmdb if it doesnt exist
if not isdir(valLmdbPath):
	print 'val lmdb not found at: %s, creating one...' % valLmdbPath
	CreateLmdb(
		valLmdbPath,
		valImageLabelMapPath,
		imageSquaredDimension
	)
else:
	print 'val lmdb found!'

# create test lmdb if it doesnt exist
if not isdir(testLmdbPath):
	print 'test lmdb not found at: %s, creating one...' % testLmdbPath
	CreateLmdb(
		testLmdbPath,
		testImageLabelMapPath,
		imageSquaredDimension
	)
else:
	print 'test lmdb found!'

# create train lmdb if it doesnt exist
if not isdir(trainLmdbPath):
	print 'train lmdb not found at: %s, creating one...' % trainLmdbPath
	makedirs(trainLmdbPath)
	CreateLmdb(
		trainLmdbPath,
		trainImageLabelMapPath,
		imageSquaredDimension
	)
else:
	print 'train lmdb found!'

workspace.ResetWorkspace(workspaceRootFolder)

labels = None
print 'loading labels'
with open(labelsPath, 'r') as f:
	labels = json.load(f)

print 'amount of labels: %d' % len(labels)

trainModel, testModel = None, None
if exists(initNetPath) and Confirm('pretrained model file found. load?'):
	trainModel = LoadTrainModel('train_model',
		trainLmdbPath, len(labels), batchSize,
		imageSquaredDimension,
		initNetPath
	)
	print 'train model loaded'

if trainModel == None:
	print 'models initialization'
	trainModel = InitTrainModel(
		'train_model',
		len(labels),
		imageSquaredDimension,
		trainLmdbPath,
		batchSize,
		10**-2
	)

print '---'
testModel = InitNonTrainingModel(
	'test_model',
	len(labels),
	imageSquaredDimension,
	testLmdbPath,
	1
)

print '---'
valModel = InitNonTrainingModel(
	'val_model',
	len(labels),
	imageSquaredDimension,
	testLmdbPath,
	1
)

print '---'

deployModel = InitDeployModel(
	'deploy_model',
	'data',
	len(labels),
	imageSquaredDimension
)

# sys.exit(0)

print 'starting training of %d iterations' % trainIters

workspace.RunNetOnce(valModel.param_init_net)
workspace.CreateNet(valModel.net)
loss, accuracy = RunModel(workspace, trainModel, trainIters, statisticsEvery, lambda i: RunValidation(workspace, valModel, i))

print 'last accuracies: '
print accuracy[-10:]

print 'last losses: '
print loss[-10:]

testLen = len(test)
print 'starting testing of %d' % testLen
workspace.RunNetOnce(testModel.param_init_net)
workspace.CreateNet(testModel.net)
loss, accuracy = RunModel(workspace, testModel, testLen, 1, lambda i: PrintStatistics(workspace, i))

if not Confirm('do y want to save model?'):
	print 'not saving model..'
	sys.exit(0)

SaveModel(workspace, deployModel, initNetPath, predictNetPath)

print 'done!'
