from os.path import isdir, isfile, join, exists
from os import makedirs
import json, sys

from PIL import Image

from caffe2.python import workspace
from caffe2.python import net_drawer
from DataHelpers import CreateLmdb, FetchRowCount, SplitImages
from ModelHelpers import (
	InitTrainModel,
	InitTestModel,
	InitDeployModel,
	ExecuteModelTraining,
	SaveModel,
	LoadTrainModel
)
from Constants import (
	imageSquaredDimension,
	batchSize,
	learningRate,
	trainLmdbPath,
	valLmdbPath,
	checkpointPath,
	labelsPath,
	imageLabelMapPath,
	trainImageLabelMapPath,
	valImageLabelMapPath,
	trainIters,
	validateEvery,
	workspaceRootFolder,
	initNetPath,
	predictNetPath
)

# check image_label_maps
if not isfile(trainImageLabelMapPath):
	train, val = SplitImages(imageLabelMapPath, 0.7)
	with open(trainImageLabelMapPath, 'w') as f:
		json.dump(train.tolist(), f, indent=2)
	with open(valImageLabelMapPath, 'w') as f:
		json.dump(val.tolist(), f, indent=2)

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

def Confirm(message):
	return raw_input(message + ' [[y]/n] ') in ['y', 'Y', 'yes', '']

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
testModel = InitTestModel(
	'test_model',
	len(labels),
	imageSquaredDimension,
	valLmdbPath,
	1
)

print '---'

deployModel = InitDeployModel(
	'deploy_model',
	'data',
	len(labels),
	imageSquaredDimension
)

# graph = net_drawer.GetPydotGraph(trainModel.net.Proto().op, 'TreeNet', rankdir='lr')
# Image.fromarray(graph.create_png()).show('TreeNet')

# graph = net_drawer.GetPydotGraphMinimal(trainModel.net.Proto().op, 'TreeNet', rankdir="lr", minimal_dependency=True)
# Image.fromarray(graph.create_png()).show('TreeNet1')

# sys.exit(0)

print 'starting training of %d iterations' % trainIters

loss, accuracy = ExecuteModelTraining(workspace, trainModel, trainIters, validateEvery)

print 'last accuracies: '
print accuracy[-10:-1]

print 'last losses: '
print loss[-10:-1]

if not Confirm('do y want to save model?'):
	print 'not saving model..'
	sys.exit(0)

SaveModel(workspace, deployModel, initNetPath, predictNetPath)

print 'done!'
