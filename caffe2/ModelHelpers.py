from caffe2.python import brew, optimizer, core, model_helper
from os.path import join
from os import makedirs
import datetime
import numpy as np
import math
from caffe2.python.predictor import mobile_exporter, predictor_exporter as pe
from caffe2.python import caffe2_pb2, workspace

from caffe2.python.modeling import initializers
from caffe2.python.modeling.parameter_info import ParameterTags

def ScaffoldModelInput(model, lmdbPath, batchSize):
	data, label = brew.db_input(
		model,
		['data', 'label'],
		batch_size=batchSize,
		db=lmdbPath,
		db_type='lmdb'
	)

	# data is already in float type.. no conversion required
	# floatData = model.Cast(dataInt, 'data_float', to=core.DataType.FLOAT)

	# channel values from 0-255 to 0-1 were already scaled in preprocessing part
	# data = model.Scale(floatData, 'data', scale=float(1. / 256))

	model.StopGradient(data, data)
	return data, label

def computeImageDimensions(height, width, kernel, stride, pad):
	new_height = ((height - kernel + (2 * pad)) / stride) + 1
	new_width = ((width - kernel + (2 * pad)) / stride) + 1
	return new_height, new_width

def getCnnModel(model, classCount, data, imageDimension, amountOfChannels=3, isTest=0):
	return ScaffoldModellCNNv6(model, classCount, data, imageDimension, amountOfChannels)
	# return ScaffoldModelCNNRepetitor(model, classCount, data, imageDimension, amountOfChannels, isTest=isTest)
	# return ScaffoldModelCNNv1(model, classCount, data, imageDimension, amountOfChannels)
	# return ScaffoldModelMLP(model, classCount, data, imageDimension, amountOfChannels)

def ScaffoldModelMLP(model, classCount, data, imageDimension, amountOfCahnnels=3):
	'''
	Doesnt seem to be working
	'''
	dataDims = imageDimension * imageDimension * amountOfCahnnels
	layerSizes = dataDims, dataDims * 2, dataDims * 2, classCount
	layer = data
	for i in range(len(layerSizes) - 1):
		layer = brew.fc(model, layer, 'fc_%d' % i, dim_in=layerSizes[i], dim_out=layerSizes[i+1])
		layer = brew.relu(model, layer, 'relu_%d' % i)
	return brew.softmax(model, layer, 'softmax')

def ScaffoldModelCNNv1(model, classCount, data, imageDimension, amountOfChannels=3):
	# layer 1
	conv1 = brew.conv(model, data, 'conv1', dim_in=amountOfChannels, dim_out=48, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(imageDimension, imageDimension, 5, 1, 2)
	print 'size after conv1: ', h, w
	maxPool1 = brew.max_pool(model, conv1, 'm_pool1', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after max_pool1: ', h, w
	relu1 = brew.relu(model, maxPool1, 'relu1')

	# layer 2
	conv2 = brew.conv(model, relu1, 'conv2', 48, 48, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size after conv2: ', h, w
	relu2 = brew.relu(model, conv2, 'relu2')
	avgPool2 = brew.average_pool(model, relu2, 'avg_pool2', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after avg_pool2: ', h, w

	# layer 3
	conv3 = brew.conv(model, avgPool2, 'conv3', 48, 64, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size after conv3: ', h, w
	relu3 = brew.relu(model, conv3, 'relu3')
	avgPool3 = brew.average_pool(model, relu3, 'avg_pool3', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after avg_pool3: ', h, w

	# last 2 fc layers
	fc1 = brew.fc(model, avgPool3, 'fc1', dim_in=64*h*w, dim_out=64)
	fc2 = brew.fc(model, fc1, 'fc2', dim_in=64, dim_out=classCount)

	# format output
	return brew.softmax(model, fc2, 'softmax')

def ScaffoldModelCNNv2(model, classCount, data, imageDimension, amountOfChannels=3):
	# layer 1
	conv1 = brew.conv(model, data, 'conv1', dim_in=amountOfChannels, dim_out=48, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(imageDimension, imageDimension, 5, 1, 2)
	print 'size after conv1: ', h, w
	max_pool1 = brew.max_pool(model, conv1, 'm_pool1', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after max_pool1: ', h, w
	relu1 = brew.relu(model, max_pool1, 'relu1')

	# layer 2
	conv2 = brew.conv(model, relu1, 'conv2', 48, 48, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size after conv2: ', h, w
	relu2 = brew.relu(model, conv2, 'relu2')
	# avg_pool2 = brew.average_pool(model, relu2, 'avg_pool2', kernel=3, stride=2)
	# h, w = compute_modified_img_dims(h, w, 3, 2, 0)
	# print 'size after avg_pool2: ', h, w

	# layer 3
	conv3 = brew.conv(model, relu2, 'conv3', 48, 64, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size after conv3: ', h, w
	relu3 = brew.relu(model, conv3, 'relu3')
	# avg_pool3 = brew.average_pool(model, relu3, 'avg_pool3', kernel=3, stride=2)
	# h, w = compute_modified_img_dims(h, w, 3, 2, 0)
	# print 'size after avg_pool3: ', h, w

	# layer 4
	conv4 = brew.conv(model, relu3, 'conv4', 64, 64, kernel=5, stride=1, pad=0)
	h, w = computeImageDimensions(h, w, 5, 1, 0)
	print 'size after conv4: ', h, w
	relu4 = brew.relu(model, conv4, 'relu4')
	avg_pool4 = brew.average_pool(model, relu4, 'avg_pool4', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after avg_pool4: ', h, w

	# layer 5
	conv5 = brew.conv(model, avg_pool4, 'conv5', 64, 64, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size after conv5: ', h, w
	relu5 = brew.relu(model, conv5, 'relu5')
	avg_pool5 = brew.average_pool(model, relu5, 'avg_pool5', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after avg_pool5: ', h, w

	# last 2 fc layers
	fc1 = brew.fc(model, avg_pool5, 'fc1', dim_in=64*h*w, dim_out=64)
	fc2 = brew.fc(model, fc1, 'fc2', dim_in=64, dim_out=classCount)

	# format output
	return brew.softmax(model, fc2, 'softmax')

def ScaffoldModelCNNv3(model, classCount, data, imageDimension, amountOfChannels=3):
	# layer 1
	conv1 = brew.conv(model, data, 'conv1', dim_in=amountOfChannels, dim_out=48, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(imageDimension, imageDimension, 5, 1, 2)
	print 'size after conv1: ', h, w
	max_pool1 = brew.max_pool(model, conv1, 'm_pool1', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after max_pool1: ', h, w
	relu1 = brew.relu(model, max_pool1, 'relu1')

	conv2 = brew.conv(model, relu1, 'conv2', 48, 48, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size after conv2: ', h, w
	relu2 = brew.relu(model, conv2, 'relu2')
	maxPool2 = brew.max_pool(model, relu2, 'avg_pool2', kernel=2, stride=1)
	h, w = computeImageDimensions(h, w, 2, 1, 0)
	print 'size after maxPool2: ', h, w

	conv3 = brew.conv(model, maxPool2, 'conv3', 48, 48, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size after conv3: ', h, w
	maxPool3 = brew.max_pool(model, conv3, 'max_pool3', kernel=3, stride=1)
	h, w = computeImageDimensions(h, w, 3, 1, 0)
	print 'size after maxPool3: ', h, w
	relu3 = brew.relu(model, maxPool3, 'relu3')

	conv4 = brew.conv(model, relu3, 'conv4', 48, 64, kernel=5, stride=2, pad=2)
	h, w = computeImageDimensions(h, w, 5, 2, 2)
	print 'size after conv4: ', h, w
	relu4 = brew.relu(model, conv4, 'rolu4')
	maxPool4 = brew.max_pool(model, relu4, 'avg_pool4', kernel=3, stride=2)
	h, w = computeImageDimensions(h, w, 3, 2, 0)
	print 'size after maxPool4: ', h, w

	# last 2 fc layers
	fc1 = brew.fc(model, maxPool4, 'fc1', dim_in=64*h*w, dim_out=64)
	fc2 = brew.fc(model, fc1, 'fc2', dim_in=64, dim_out=classCount)

	# format output
	return brew.softmax(model, fc2, 'softmax')

def ScaffoldModelCNNv4(model, classCount, data, imageDimension, amountOfChannels=3):
	conv1 = brew.conv(model, data, 'conv1', amountOfChannels, 16, 3, stride=1, pad=1)
	h, w = computeImageDimensions(imageDimension, imageDimension, 3, 1, 1)
	print 'size: ', h, w
	relu1 = brew.relu(model, conv1, 'relu1')

	conv2 = brew.conv(model, relu1, 'conv2', 16, 16, 3, stride=1, pad=1)
	h, w = computeImageDimensions(h, w, 3, 1, 1)
	print 'size: ', h, w
	relu2 = brew.relu(model, conv2, 'relu2')

	conv3 = brew.conv(model, relu2, 'conv3', 16, 16, 5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size: ', h, w
	maxPool3 = brew.max_pool(model, conv3, 'maxPool3', kernel=2, stride=2)
	h, w = computeImageDimensions(h, w, 2, 2, 0)
	print 'size: ', h, w

	conv4 = brew.conv(model, maxPool3, 'conv4', 16, 32, 5, stride=1, pad=1)
	h, w = computeImageDimensions(h, w, 5, 1, 1)
	print 'size: ', h, w
	relu4 = brew.relu(model, conv4, 'relu4')

	conv5 = brew.conv(model, relu4, 'conv5', 32, 32, 5, stride=1, pad=1)
	h, w = computeImageDimensions(h, w, 5, 1, 1)
	print 'size: ', h, w
	relu5 = brew.relu(model, conv5, 'relu5')
	maxPool5 = brew.max_pool(model, relu5, 'maxPool5', kernel=2, stride=2)
	h, w = computeImageDimensions(h, w, 2, 2, 0)
	print 'size: ', h, w

	conv6 = brew.conv(model, maxPool5, 'conv6', 32, 32, 5, stride=1, pad=1)
	h, w = computeImageDimensions(h, w, 5, 1, 1)
	print 'size: ', h, w
	relu6 = brew.relu(model, conv6, 'relu6')

	conv7 = brew.conv(model, relu6, 'conv7', 32, 32, 5, stride=1, pad=1)
	h, w = computeImageDimensions(h, w, 5, 1, 1)
	print 'size: ', h, w
	relu7 = brew.relu(model, conv7, 'relu7')

	conv8 = brew.conv(model, relu7, 'conv8', 32, 64, 5, stride=1, pad=1)
	h, w = computeImageDimensions(h, w, 5, 1, 1)
	print 'size: ', h, w
	maxPool8 = brew.max_pool(model, conv8, 'maxPool8', kernel=2, stride=2)
	h, w = computeImageDimensions(h, w, 2, 2, 0)
	print 'size: ', h, w
	relu8 = brew.relu(model, maxPool8, 'relu8')

	conv9 = brew.conv(model, relu8, 'conv9', 64, 64, 1, stride=1)
	h, w = computeImageDimensions(h, w, 1, 1, 0)
	print 'size: ', h, w
	relu9 = brew.relu(model, conv9, 'relu9')

	fc10 = brew.fc(model, relu9, 'fc10', dim_in=64*h*w, dim_out=64)
	fc11 = brew.fc(model, fc10, 'fc11', dim_in=64, dim_out=32)
	fc12 = brew.fc(model, fc11, 'fc12', dim_in=32, dim_out=classCount)

	return brew.softmax(model, fc12, 'softmax')

def ScaffoldModelCNNv5(model, classCount, data, imageDimension, amountOfChannels=3):
	conv1 = brew.conv(model, data, 'conv1', amountOfChannels, 96, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(imageDimension, imageDimension, 5, 1, 2)
	print 'size: ', h, w
	maxPool1 = brew.max_pool(model, conv1, 'max_pool1', kernel=2, stride=2)
	h, w = computeImageDimensions(h, w, 2, 2, 0)
	print 'size: ', h, w
	relu1 = brew.relu(model, maxPool1, 'relu1')

	conv2 = brew.conv(model, relu1, 'conv2', 96, 256, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size: ', h, w
	maxPool2 = brew.max_pool(model, conv2, 'max_pool2', kernel=2, stride=2)
	h, w = computeImageDimensions(h, w, 2, 2, 0)
	print 'size: ', h, w
	relu2 = brew.relu(model, maxPool2, 'relu2')

	conv3 = brew.conv(model, relu2, 'conv3', 256, 384, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size: ', h, w

	conv4 = brew.conv(model, conv3, 'conv4', 384, 384, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size: ', h, w

	conv5 = brew.conv(model, conv4, 'conv5', 384, 256, kernel=5, stride=1, pad=2)
	h, w = computeImageDimensions(h, w, 5, 1, 2)
	print 'size: ', h, w
	maxPool5 = brew.max_pool(model, conv5, 'max_pool5', kernel=2, stride=2)
	h, w = computeImageDimensions(h, w, 2, 2, 0)
	print 'size: ', h, w

	fc6 = brew.fc(model, maxPool5, 'fc6', dim_in=256*h*w, dim_out=128)
	fc7 = brew.fc(model, fc6, 'fc7', dim_in=128, dim_out=64)
	fc8 = brew.fc(model, fc7, 'fc8', dim_in=64, dim_out=classCount)

	return brew.softmax(model, fc8, 'softmax')

def ScaffoldModellCNNv6(model, classCount, data, imageDimension, amountOfChannels=3):
	conv1 = brew.conv(model,'data', 'conv1', amountOfChannels, 20, kernel=5, stride=1, pad=0)
	imgDim = computeImageDimensions(imageDimension, imageDimension, 5, 1, 0)[0]
	pool1 = brew.max_pool(model, conv1, 'pool1', kernel=2, stride=2)

	conv2 = brew.conv(model, pool1, 'conv2', 20, 50, kernel=5, stride=1, pad=0)
	imgDim = computeImageDimensions(imgDim, imgDim, 5, 1, 0)[0]
	pool2 = brew.max_pool(model, conv2, 'pool2', kernel=2, stride=2)

	fc3 = brew.fc(model, pool2, 'fc3', dim_in=50 * (imgDim ** 2), dim_out=500)
	fcRelu3 = brew.relu(model, fc3, 'fc_relu')
	pred = brew.fc(model, fcRelu3, 'pred', dim_in=500, dim_out=classCount)
	return brew.softmax(model, pred, 'softmax')

def ScaffoldModelCNNRepetitor(model, classCount, data, imageDimension, amountOfChannels=3, isTest=0):
	dims = amountOfChannels, 8, 10, 12

	convKernel = 3
	convStride = 1
	convPad = 1

	poolingKernel = 2
	poolingStride = 2

	imageDim = imageDimension
	poolingFrom = 5
	layer = data
	for i in range(len(dims) - 1):
		# if i == 1:
		# 	layer = brew.dropout(model, layer, 'drop_%d' % i, ratio=0.4, is_test=isTest)

		layer = brew.conv(
			model, layer, 'conv_%d' % i, dim_in=dims[i],
			dim_out=dims[i + 1], kernel=convKernel, stride=convStride, pad=convPad)
		imageDim = computeImageDimensions(imageDim, imageDim, convKernel, convStride, convPad)[0]
		layer = brew.relu(model, layer, 'relu_%d' % i)
		if i > poolingFrom:
			layer = brew.average_pool(model, layer, 'avg_pool_%d' % i, kernel=poolingKernel, stride=poolingStride)
			imageDim = computeImageDimensions(imageDim, imageDim, poolingKernel, poolingStride, 0)[0]

	fc = brew.fc(model, layer, 'fc_%d' % len(dims), dim_in=(imageDim ** 2) * dims[-1], dim_out=classCount)
	return brew.softmax(model, fc, 'softmax')

def ScaffoldModelBackpropagation(model, softmax, label, learningRate):
	# loss function - tells how wrong the prediction was
	crossEntropy = model.LabelCrossEntropy([softmax, label], 'cross_entropy')
	# expected loss (how to find out more on this step)
	loss = model.AveragedLoss(crossEntropy, 'loss')
	ScaffoldModelAccuracyMeter(model, softmax, label)
	# add gradient operator used for backpropagation
	model.AddGradientOperators([loss])
	# lastly construct stochastic gradient descent for learning
	optimizer.build_sgd(
		model,
		base_learning_rate=learningRate,
		policy='step',
		stepsize=1,
		gamma=0.999
		# momentum=0.9,
		# weight_decay=0.004
	)

def ScaffoldModelTrainingOperators(model, softmax, label, learningRate):
	crossEntropy = model.LabelCrossEntropy([softmax, label], 'cross_entropy')
	loss = model.AveragedLoss(crossEntropy, 'loss')
	ScaffoldModelAccuracyMeter(model, softmax, label)
	model.AddGradientOperators([loss])
	ITER = brew.iter(model, 'iter')
	learningRate = model.LearningRate(
		ITER, 'lr', base_lr=learningRate, policy='step', stepsize=1, gamma=0.999
	)
	one = model.param_init_net.ConstantFill([], 'one', shape=[1], value=1.0)
	for param in model.params:
		paramGrad = model.param_to_grad[param]
		model.WeightedSum([param, one, paramGrad, learningRate], param)

def ScaffoldModelTrainingOPeratorsSqueezenet(model, softmax, label, learningRate):
	xent = model.LabelCrossEntropy([softmax, label], "xent")
	loss = model.AveragedLoss(xent, "loss")
	ScaffoldModelAccuracyMeter(model, softmax, label)
	model.AddGradientOperators([loss])
	opt = optimizer.build_sgd(model, base_learning_rate=learningRate)
	for param in model.GetOptimizationParamInfo():
			opt(model.net, model.param_init_net, param)

def ScaffoldModelAccuracyMeter(model, softmax, label):
	return brew.accuracy(model, [softmax, label], 'accuracy')

def ScaffoldModelBackupOperators(model):
	model.Print('loss', [], to_file=1)
	model.Print('accuracy', [], to_file=1)

	for param in model.params:
		model.Summarize(param, [], to_file=1)
		model.Summarize(model.param_to_grad[param], [], to_file=1)

def ScaffoldModelCheckpoints(model, checkpointFolder, every):
	newCheckpointFolder = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
	newCheckpointFolder = join(checkpointFolder, newCheckpointFolder)

	print 'check point folder: ', newCheckpointFolder
	makedirs(newCheckpointFolder)

	iter = brew.iter(model, 'iterations')
	model.Checkpoint([iter] + model.params, [], db=join(newCheckpointFolder, 'dataset_checkpoint_%05d.lmdb'), db_type='lmdb', every=every)

def InscribeDeviceOptionsToModel(model, deviceOption):
	# Clear op-specific device options and set global device option.
	for net in ("net", "param_init_net"):
		netDef = getattr(model, net).Proto()
		netDef.device_option.CopyFrom(deviceOption)
		for op in netDef.op:
			# Some operators are CPU-only.
			if op.output[0] not in ("optimizer_iteration", "iteration_mutex"):
						op.ClearField("device_option")
						op.ClearField("engine")
		setattr(model, net, core.Net(netDef))

def CreateModel(
	name,
	labelsCount,
	imageDimension,
	lmdbPath,
	batchSize,
	learningRate=None,
	initParams=True,
	scaffoldAccuracy=False,
	isTest=0):
	argScope = {
		'order': 'NCHW',
		'use_cudnn': 1
	}
	with core.DeviceScope(core.DeviceOption(caffe2_pb2.CUDA, 0)):
		model = model_helper.ModelHelper(name=name, arg_scope=argScope, init_params=initParams)

		# model.net.RunAllOnGpu()
		# model.param_init_net.RunAllOnGpu()

		# data input
		data, label = ScaffoldModelInput(model, lmdbPath, batchSize)
		# CNN
		softmax = getCnnModel(model, labelsCount, data, imageDimension, 3, isTest=isTest)

		if learningRate != None:
			ScaffoldModelBackpropagation(model, softmax, 'label', learningRate)
			# ScaffoldModelTrainingOperators(model, softmax, label, learningRate)

		if scaffoldAccuracy:
			ScaffoldModelAccuracyMeter(model, softmax, label)

		# ScaffoldModelBackupOperators(model)

	return model

def CreateDeployModel(name, data, labelsCount, imageDimension):
	model = model_helper.ModelHelper(name=name, arg_scope={
		'order': 'NCHW'
	}, init_params=False)

	getCnnModel(model, labelsCount, data, imageDimension, 3)

	return model

def InitModel(model):
	workspace.RunNetOnce(model.param_init_net)
	workspace.CreateNet(model.net)

def RunModel(model, iters, logEvery, statisticsHandler=None, setupHandler=None):
	workspace.RunNetOnce(model.param_init_net)
	workspace.CreateNet(model.net, overwrite=True)

	if type(setupHandler) != type(None):
		setupHandler()

	acc = np.zeros(iters/logEvery)
	loss = np.zeros(iters/logEvery)
	iterList = np.zeros(iters/logEvery)
	valCount = 0

	for i in range(iters/logEvery):
		workspace.RunNet(model.net, logEvery)
		if type(statisticsHandler) != type(None):
			statisticsHandler(i * logEvery)

		acc[valCount] = workspace.FetchBlob('accuracy')
		loss[valCount] = workspace.FetchBlob('loss')
		iterList[valCount] = i

		valCount += 1
	
	return acc, loss, iterList

def SaveModel(workspace, deployModel, initNetPath, predictNetPath):
	workspace.RunNetOnce(deployModel.param_init_net)
	workspace.CreateNet(deployModel.net, overwrite=True)

	initNet, predictNet = mobile_exporter.Export(workspace, deployModel.net, deployModel.params)

	with open(initNetPath, 'wb') as f:
		f.write(initNet.SerializeToString())
	with open(predictNetPath, 'wb') as f:
		f.write(predictNet.SerializeToString())
	
	print 'model files are saved at: %s and %s' % (initNetPath, predictNetPath)

def LoadPredictor(workspace, initNetPath, predictNetPath):
	initNet, predictNet = None, None

	with open(initNetPath, 'rb') as f:
		initNet = f.read()
	with open(predictNetPath, 'rb') as f:
		predictNet = f.read()
	
	return workspace.Predictor(initNet, predictNet)

def LoadTrainModel(name,
	lmdbPath, classCount, batchSize, imageDimension,
	initNetPath, learningRate=10**-2):

	model = model_helper.ModelHelper(name, init_params=False, arg_scope={
	
		'order': 'NCHW'
	})

	data, _ = ScaffoldModelInput(model, lmdbPath, batchSize)

	softmax = getCnnModel(model, classCount, data, imageDimension, 3)

	init_net_pb = caffe2_pb2.NetDef()
	with open(initNetPath, 'rb') as f:
		init_net_pb.ParseFromString(f.read())
	model.param_init_net = model.param_init_net.AppendNet(core.Net(init_net_pb))

	ScaffoldModelBackpropagation(model, softmax, 'label', learningRate)
	# ScaffoldModelTrainingOperators(model, softmax, label, lear(ningRate)

	if len(model.GetOptimizationParamInfo()) == 0:
		print 'Error in setting up Stochastic gradient descent'

	return model

def LoadPretrainedSqueezenetModel(name,
	lmdbPath, classCount, batchSize, imageDimension,
	initNetPath, predictNetPath, deviceOpts, outputDims, paramsToLearn = None,
	learningRate=10**-2):

	model = model_helper.ModelHelper(name)

	predictNetPb = caffe2_pb2.NetDef()
	with open(predictNetPath, 'rb') as f:
		predictNetPb.ParseFromString(f.read())
	
	initNetPb = caffe2_pb2.NetDef()
	with open(initNetPath, 'rb') as f:
		initNetPb.ParseFromString(f.read())

	with core.DeviceScope(deviceOpts):
		data, label = ScaffoldModelInput(model, lmdbPath, batchSize)

		model.net = core.Net(predictNetPb)
		# dims param has wrong values...
		model.Squeeze('softmaxout', 'softmax', dims=[2, 3])

		for op in initNetPb.op:
			paramName = op.output[0]
			if paramsToLearn == None or paramName in paramsToLearn:
				tags = (ParameterTags.WEIGHT if paramName.endswith('_w') else ParameterTags.BIAS)
				model.create_param(param_name=paramName, shape=op.arg[0], initializer=initializers.ExternalInitializer(), tags=tags)
		
		# 'removing conv10_w and conv10_b' from init net
		initNetPb.op.pop(51)
		initNetPb.op.pop(50)

		# reinitialize conv10
		model.param_init_net = core.Net(initNetPb)
		model.param_init_net.XavierFill([], 'conv10_w', shape=[classCount, 512, 1, 1])
		model.param_init_net.ConstantFill([], 'conv10_b', shape=[classCount])

		ScaffoldModelTrainingOPeratorsSqueezenet(model, 'softmax', label, learningRate)
		InscribeDeviceOptionsToModel(model, deviceOpts)

	return model
