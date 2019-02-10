from os.path import expanduser, join, isfile
import json, numpy as np

from caffe2.python import core, workspace
from caffe2.proto import caffe2_pb2 as c2p2

from ModelHelpers import (
	TranslateAlexNetOrVGG19,
	RunModel,
	InitModel
)

from Methods import PrintStatistics
from DatasetHelpers import LmdbDatasetWrapper
from Constants import (
	labelsPath
)


lmdbPath = expanduser('~/workbench/tree-images/workspace/lmdb/train-dataset-lmdb-227')
inputModelFolderPath = expanduser('~/workbench/caffe2-models/bvlc_alexnet')

targetPath = expanduser('~/workbench/git/TreeRecognitionProject/caffe2/output')
initNetPath = join(targetPath, 'init_net.pb')
predNetPath = join(targetPath, 'predict_net.pb')

workspace.ResetWorkspace()

with open(labelsPath, 'r') as f:
	labels = json.load(f)

devOps = c2p2.DeviceOption()
devOps.device_type = c2p2.PROTO_CUDA
devOps.device_id = 0
argScope = {
	'order': 'NCHW',
	'use_cudnn': True
}

# if isfile(initNetPath) and isfile(predNetPath):
# 	squeezenetModel, deployPredNetPb = LoadCustomSqueezenetModel(
# 		'squeezenet',
# 		initNetPath,
# 		predNetPath,
# 		devOps,
# 		argScope
# 	)
# else:
model, deployPredNetPb = TranslateAlexNetOrVGG19(
	'alexnet',
	len(labels),
	join(inputModelFolderPath, 'init_net.pb'),
	join(inputModelFolderPath, 'predict_net.pb'),
	devOps,
	argScope
)

print 'model translated'


datasetWrapper = LmdbDatasetWrapper(lmdbPath, 48, 227, newImageSize=224)
datasetWrapper.Open()

# initialize input blobs
data, label = datasetWrapper[0]
workspace.FeedBlob('data', np.stack(data).astype(np.float32), device_option=devOps)
workspace.FeedBlob('label', np.stack([label]).astype(np.int32), device_option=devOps)

def FeedData(batchIndex):
	datas, labels = datasetWrapper.GetBatch(batchIndex)
	workspace.FeedBlob('data', datas, device_option=devOps)
	workspace.FeedBlob('label', labels, device_option=devOps)

print 'lmdb wrapper initialized'

# create nets
InitModel(model)

print 'model initialized'

acc, loss, iterList = RunModel(
	model,
	10,
	1,
	lambda i: FeedData(i),
	PrintStatistics
)

