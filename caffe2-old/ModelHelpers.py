from caffe2.python import brew, optimizer, core, model_helper, workspace
from os.path import join
from os import makedirs
import datetime
import numpy as np
import math
from caffe2.python.predictor import mobile_exporter, predictor_exporter as pe
from caffe2.proto import caffe2_pb2 as c2p2

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

	# # channel values from 0-255 to 0-1 were already scaled in preprocessing part
	# data = model.Scale(floatData, 'data', scale=float(1. / 256))

	# model.StopGradient(data, data)
	return data, label

def recalculateDim(size, kernel, stride, pad):
	nSize = ((size - kernel + (2 * pad)) / stride) + 1
	return nSize

def getCnnModel(model, classCount, data, imageDimension, amountOfChannels=3, isTest=0):
	return ScaffoldModelCNN_AlexNet(model, classCount, data, imageDimension, amountOfChannels)
	# return ScaffoldModelCNNRepetitor(model, classCount, data, imageDimension, amountOfChannels, isTest=isTest)
	# return ScaffoldModelCNNv1(model, classCount, data, imageDimension, amountOfChannels)
	# return ScaffoldModelMLP(model, classCount, data, imageDimension, amountOfChannels)

def ScaffoldModelCNN_AlexNet(model, classCount, data, imageDimension, amountOfChannels):
	brew.conv(model, data, 'conv1', amountOfChannels, 96, 11, stride=4, pad=0)
	brew.relu(model, 'conv1', 'conv1')
	brew.max_pool(model, 'norm1', 'pool1', kernel=3, stride=2, pad=0)

	brew.conv(model, 'pool1', 'conv2', 48, 256, 5, stride=1, pad=2)
	brew.relu(model, 'conv2', 'conv2')
	brew.max_pool(model, 'norm2', 'pool2', kernel=3, stride=2, pad=0)

	brew.conv(model, 'pool2', 'conv3', 256, 384, 3, stride=1, pad=1)
	brew.relu(model, 'conv3', 'conv3')

	brew.conv(model, 'conv3', 'conv4', 192, 384, 3, stride=1, pad=1)
	brew.relu(model, 'conv4', 'conv4')

	brew.conv(model, 'conv4', 'conv5', 192, 256, 3, stride=1, pad=1)
	brew.relu(model, 'conv5', 'conv5')
	brew.max_pool(model, 'conv5', 'pool5', kernel=3, stride=2, pad=1)

	brew.fc(model, 'pool5', 'fc6', 9216, 4096)
	brew.relu(model, 'fc6', 'fc6')
	brew.fc(model, 'fc6', 'fc7', 4096, 4096)
	brew.relu(model, 'fc7', 'fc7')
	brew.fc(model, 'fc7', 'fc8', 4096, 1000)

	return brew.softmax(model, 'fc8', 'softmax')

def ScaffoldModelBackpropagation(model, softmax, label, learningRate):
	# loss function - tells imageSizeow wrong the prediction was
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

def ScaffoldModelTrainingOperators(model, softmax, label, learningRate, devOps=None):
	# with core.DeviceScope(core.DeviceOption(c2p2.PROTO_CUDA, 0)):
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
		'use_cudnn': True
	}
	with core.DeviceScope(core.DeviceOption(c2p2.PROTO_CUDA, 0)):
		model = model_helper.ModelHelper(name=name, arg_scope=argScope, init_params=initParams)
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

def InitModel(model, overwrite=True):
	workspace.RunNetOnce(model.param_init_net)
	workspace.CreateNet(model.net, overwrite=overwrite)

def RunModel(model, iters, logEvery, beforeExecution=None, statisticsHandler=None, setupHandler=None):
	if type(setupHandler) != type(None):
		setupHandler()

	acc = np.zeros(iters/logEvery)
	loss = np.zeros(iters/logEvery)
	iterList = np.zeros(iters/logEvery)
	valCount = 0

	for i in range(iters):
		if beforeExecution != None:
			beforeExecution(i)
		workspace.RunNet(model.net)

		if i % logEvery == 0 and type(statisticsHandler) != type(None):
			statisticsHandler(i)

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
	
		'order': 'NCHW'})

	data, _ = ScaffoldModelInput(model, lmdbPath, batchSize)

	softmax = getCnnModel(model, classCount, data, imageDimension, 3)

	init_net_pb = c2p2.NetDef()
	with open(initNetPath, 'rb') as f:
		init_net_pb.ParseFromString(f.read())
	model.param_init_net = model.param_init_net.AppendNet(core.Net(init_net_pb))

	ScaffoldModelBackpropagation(model, softmax, 'label', learningRate)
	# ScaffoldModelTrainingOperators(model, softmax, label, lear(ningRate)

	if len(model.GetOptimizationParamInfo()) == 0:
		print 'Error in setting up Stochastic gradient descent'

	return model

def LoadCustomSqueezenetModel(name,
	initNetPath, predictNetPath, deviceOps, argScope,
	learningRate=10**-2, freezeOpsUntil='conv10'):

	model = model_helper.ModelHelper(name, arg_scope=argScope, init_params=False)

	predNetPb = c2p2.NetDef()
	with open(predictNetPath, 'rb') as f:
		predNetPb.ParseFromString(f.read())
	
	initNetPb = c2p2.NetDef()
	with open(initNetPath, 'rb') as f:
		initNetPb.ParseFromString(f.read())

	opsFreezed = True
	for op in initNetPb.op:
		paramName = op.output[0]
		if opsFreezed and freezeOpsUntil in paramName:
			opsFreezed = False
		if not opsFreezed and paramName.endswith('_w') or paramName.endswith('_b'):
			tags = (ParameterTags.WEIGHT if paramName.endswith('_w') else ParameterTags.BIAS)
			model.create_param(param_name=paramName, shape=op.arg[0], initializer=initializers.ExternalInitializer(), tags=tags)
	
	# removing conv10_w and conv10_b from init net
	# initNetPb.op.pop(51)
	# initNetPb.op.pop(50)

	model.param_init_net = core.Net(initNetPb)
	model.net = core.Net(predNetPb)
	model.Squeeze('softmaxout', 'softmax', dims=[2, 3])

	ScaffoldModelTrainingOperators(model, 'softmax', 'label', learningRate)

	return model, predNetPb

def TranslateSqueezenetModel(name, classCount, initNetPath, predictNetPath, devOps, argScope,
	learningRate=10**-2):

	predNetPb = c2p2.NetDef()
	with open(predictNetPath, 'rb') as f:
		predNetPb.ParseFromString(f.read())
	
	initNetPb = c2p2.NetDef()
	with open(initNetPath, 'rb') as f:
		initNetPb.ParseFromString(f.read())

	model = model_helper.ModelHelper(name, arg_scope=argScope, init_params=False)

	for op in initNetPb.op:
		if op.output[0] in ['conv10_w', 'conv10_b']:
			tag = (ParameterTags.WEIGHT if op.output[0].endswith('_w') else ParameterTags.BIAS)
			# create params inside model
			model.create_param(op.output[0], op.arg[0], initializers.ExternalInitializer(), tags=tag)
	
	# remove conv10_w and conv10_b ops from protobuf - ids -> 50,51
	# these ops were added to the model below -> XavierFill, ConstantFill
	initNetPb.op.pop(50)
	initNetPb.op.pop(50)

	fixInPlaceOps(predNetPb.op)

	model.net = core.Net(predNetPb)
	model.Squeeze('softmaxout', 'softmax', dims=[2, 3])

	model.param_init_net = core.Net(initNetPb)
	model.param_init_net.XavierFill([], 'conv10_w', shape=[classCount, 512, 1, 1])
	model.param_init_net.ConstantFill([], 'conv10_b', shape=[classCount])

	ScaffoldModelTrainingOperators(model, 'softmax', 'label', learningRate)

	# InscribeDeviceOptionsToModel(model, devOps)

	return model, core.Net(predNetPb)

def TranslateAlexNetOrVGG19(name, classCount, initNetPath, predictNetPath, devOps, argScope, learningRate=10**-2):
	model = model_helper.ModelHelper(name, arg_scope=argScope, init_params=False)

	initNetPb = c2p2.NetDef()
	with open(initNetPath, 'rb') as f:
		initNetPb.ParseFromString(f.read())

	for op in initNetPb.op:
		if op.output[0] == 'fc8_w':
			for arg in op.arg:
				if arg.name == 'shape':
					arg.ClearField('ints')
					arg.ints.extend([classCount, 4096])
				elif arg.name == 'values':
					arg.ClearField('floats')
					arg.floats.extend(np.random.normal(0, .1, 4096*classCount)) # gaussian curve
		elif op.output[0] == 'fc8_b':
			for arg in op.arg:
				if arg.name == 'shape':
					arg.ClearField('ints')
					arg.ints.extend([classCount])
				elif arg.name == 'values':
					arg.ClearField('floats')
					arg.floats.extend(np.zeros((classCount,)).astype(np.float32))

	for op in initNetPb.op:
		if op.output[0] in ['fc8_w', 'fc8_b']:
			tag = (ParameterTags.BIAS if op.output[0].endswith('_b') else ParameterTags.WEIGHT)
			model.create_param(op.output[0], op.arg[0], initializers.ExternalInitializer(), tags=tag)

	model.param_init_net = core.Net(initNetPb)

	predNetPb = c2p2.NetDef()
	with open(predictNetPath, 'rb') as f:
		predNetPb.ParseFromString(f.read())

	fixInPlaceOps(predNetPb.op)
	model.net = core.Net(predNetPb)

	ScaffoldModelTrainingOperators(model, 'prob', 'label', learningRate, devOps)

	return model, predNetPb

def fixInPlaceOps(ops):
	opsLen = len(ops)
	i = 0
	while i < opsLen:
		op = ops[i]
		if op.input[0] == op.output[0]:
			i = _fixInPlaceOpsRecursive(ops, opsLen, i, op.output[0])
		i = i + 1

def _fixInPlaceOpsRecursive(ops, opsLen, index, originalOpName, iteration=0):
	newOpName = '%s___%d' % (originalOpName, iteration)
	if ops[index].output[0] == originalOpName:
		ops[index].output[0] = newOpName
	if iteration != 0:
		ops[index].input[0] = '%s___%d' % (originalOpName, iteration - 1)
	if index + 1 < opsLen and ops[index + 1].input[0] == originalOpName:
		index = _fixInPlaceOpsRecursive(ops, opsLen, index + 1, originalOpName, iteration + 1)
	return index