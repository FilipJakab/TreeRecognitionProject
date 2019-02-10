for op in initProto.op:
	param_name = op.output[0]
	if param_name in ['conv10_w', 'conv10_b']:
		tags = (ParameterTags.WEIGHT if param_name.endswith("_w")
			else ParameterTags.BIAS)
		model.create_param(
			param_name=param_name,
			shape=op.arg[0],
			initializer=initializers.ExternalInitializer(),
			tags=tags
		)

for op in initProto.op:
	print op.output


brew.db_input(
	model,
	['data', 'label'],
	batch_size=32,
	db='lmdbPath',
	db_type='lmdb'
)

def updateDims(size, kernel, stride, pad):
	nSize = ((size - kernel + (2 * pad)) / stride) + 1
	return nSize

imgSize = 227
for op in predNet.op:
	if op.type not in ['Conv', 'AveragePool', 'MaxPool']:
		continue
	kernel, stride, pad = 0, 0, 0
	print op.output
	for arg in op.arg:
		if arg.name == 'kernel':
			kernel = arg.i
		elif arg.name == 'stride':
			stride = arg.i
		elif arg.name == 'pad':
			pad = arg.i
	print kernel, stride, pad
	imgSize = updateDims(imgSize, kernel, stride, pad)
	print 'new size: ', imgSize


for op in predDef.op:
	print op.type


predDef.ClearField('external_output')
predDef.external_output.extend(['softmax'])

model.net = core.Net(predDef)
brew.softmax(model, 'conv10', 'softmax')

with open('init_net.pb', 'rb') as f:
	initNet = c2p2.NetDef()
	initNet.ParseFromString(f.read())

with open('predict_net.pb', 'rb') as f:
	predNet = c2p2.NetDef()
	predNet.ParseFromString(f.read())

model = model_helper.ModelHelper('x')

for i, op in enumerate(predNet.op):
	if op.output[0] == 'softmaxout':
		predNet.op.pop(i)

predNet.ClearField('external_output')
predNet.external_output.extend(['softmax'])
model.param_init_net = core.Net(initNet)
model.net = core.Net(predNet)
brew.softmax(model, 'conv10', 'softmax')









from caffe2.python import workspace, brew, core, model_helper, optimizer
from caffe2.proto import caffe2_pb2 as c2p2
from caffe2.python.modeling.parameter_info import ParameterTags
from caffe2.python.modeling import initializers
from caffe2.python.predictor import mobile_exporter

with open('init_net.pb', 'rb') as f:
	initPb = c2p2.NetDef()
	initPb.ParseFromString(f.read())

with open('predict_net.pb', 'rb') as f:
	predPb = c2p2.NetDef()
	predPb.ParseFromString(f.read())

with core.DeviceScope(core.DeviceOption(c2p2.CUDA, 0)):
	model = model_helper.ModelHelper('x', arg_scope={
		'order': 'NCHW',
		'use_cudnn': True
	})
	model.net = core.Net(predPb)
	model.Squeeze('softmaxout', 'softmax', dims=[2, 3])
	for op in initPb.op:
		if op.output[0] in ['conv10_w', 'conv10_b']:
			tags = (ParameterTags.BIAS if op.output[0].endswith('_b') else ParameterTags.WEIGHT)
			model.create_param(param_name=op.output[0], shape=op.arg[0], initializer=initializers.ExternalInitializer(), tags=tags)
	
	# _ = initPb.op.pop(50) # conv10_w and _b
	# _ = initPb.op.pop(50)
	
	model.param_init_net = core.Net(initPb)
	model.param_init_net.XavierFill([], 'conv10_w', shape=[4, 512, 1, 1])
	model.param_init_net.ConstantFill([], 'conv10_b', shape=[4])
	xent = model.LabelCrossEntropy(['softmax', 'label'], "xent")
	loss = model.AveragedLoss(xent, 'loss')
	brew.accuracy(model, ['softmax', 'label'], 'accuracy')
	_ = model.AddGradientOperators([loss])
	opt = optimizer.build_sgd(model, base_learning_rate=10**-2)
	model.GetOptimizationParamInfo()
	for param in model.GetOptimizationParamInfo():
		opt(model.net, model.param_init_net, param)

workspace.RunNetOnce(model.param_init_net)
workspace.FeedBlob('label', 'sample text')
workspace.CreateNet(model.net, overwrite=True)

init, pred = mobile_exporter.Export(workspace, model.net, model.params)









model = model_helper.ModelHelper('xx')
def recalculateDim(size, kernel, stride, pad):
	nSize = ((size - kernel + (2 * pad)) / stride) + 1
	return nSize

s = 224
dims = 3, 10, 10, 10, 10, 20, 20, 20, 64, 128, 3
layer = 'data'
for i in range(10):
	layer = brew.conv(model, layer, 'conv_%d' % i, dim_in=dims[i], dim_out=dims[i + 1], kernel=5, stride=2)
	s = recalculateDim(s, 5, 2, 0)
	layer = brew.relu(model, layer, 'relu_%d' % i)
	if i % 3 == 0:
		layer = brew.max_pool(model, layer, 'pool_%d' % i, kernel=2, stride=2)
		s = recalculateDim(s, 2, 2, 0)


layer = brew.fc(model, layer, 'last_fc', dim_in=s*s*dims[-2], dim_out=dims[-1])
softmax = brew.softmax(model, layer, 'softmax')










for op in predPb.op:
	print op.input[0], ' -> ', op.output[0]

for op in initPb.op[-8:]:
	print op.output[0], op.arg[0]
	if op.output[0] in ['fc8_w', 'fc8_b']:




import lmdb
from caffe2.proto import caffe2_pb2 as c2p2
env = lmdb.open('/home/filip/workbench/tree-images/workspace/lmdb/train-augmented-dataset-lmdb-227')
t = env.begin(write=False)
c = t.cursor()
c.first()

tp = c2p2.TensorProtos()
tp.ParseFromString(c.item()[1])

tp.float_data[:10]





import json
from skimage.io import imread
from os.path import join
with open('/home/filip/workbench/tree-images/feature_labels_train.json', 'r') as f:
	data = json.load(f)



toDel = []
for i, pair in enumerate(data):
	img = imread(join('/home/filip/workbench/tree-images/', pair[0]))
	if len(img.shape) != 3:
		print 'image: ', pair[0], 'is not colorful..'
		toDel.append(i)

for d in toDel:
	print data[d], ' is to be deleted'




# model builder
# prints brews' functions from pred's pb files
from caffe2.python import workspace, brew, core, model_helper, optimizer
from caffe2.proto import caffe2_pb2 as c2p2
from caffe2.python.modeling.parameter_info import ParameterTags
from caffe2.python.modeling import initializers
from caffe2.python.predictor import mobile_exporter

with open('init_net.pb', 'rb') as f:
	initPb = c2p2.NetDef()
	initPb.ParseFromString(f.read())


with open('predict_net.pb', 'rb') as f:
	predPb = c2p2.NetDef()
	predPb.ParseFromString(f.read())


brewMethods = {
	'Conv': lambda inOp, outOp:
		"brew.conv(model, '%s', '%s', %d, %d, %d, stride=%d, pad=%d)"
			% (inOp, outOp, initShapes[outOp][1], initShapes[outOp][0], kernel, stride, pad),
	'MaxPool': lambda inOp, outOp:
		"brew.max_pool(model, '%s', '%s', kernel=%d, stride=%d, pad=%d)"
			% (inOp, outOp, kernel, stride, pad),
	'AveragePool': lambda inOp, outOp:
		"brew.average_pool(model, '%s', '%s', kernel=%d, stride=%d, pad=%d)"
			% (inOp, outOp, kernel, stride, pad),
	'Relu': lambda inOp, outOp: "brew.relu(model, '%s', '%s')"
			% (inOp, outOp),
	'FC': lambda inOp, outOp: "brew.fc(model, '%s', '%s', %d, %d)"
			% (inOp, outOp, initShapes[outOp][1], initShapes[outOp][0])
}

initShapes = {}
for op in initPb.op:
	opName = '_'.join(op.output[0].split('_')[:-1])
	if opName in initShapes.keys():
		continue
	initShapes[opName] = op.arg[0].ints


for op in predPb.op:
	if op.type in brewMethods.keys():
		inOp = op.input[0]
		outOp = op.output[0]
		for arg in op.arg:
			if arg.name == 'kernel':
				kernel = arg.i
			elif arg.name == 'stride':
				stride = arg.i
			elif arg.name == 'pad':
				pad = arg.i
		print brewMethods[op.type](inOp, outOp)
	else:
		print op.type, ' is not supported'

