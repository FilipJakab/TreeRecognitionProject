from os.path import expanduser, join
import json, numpy as np

from caffe2.python import core, workspace
from caffe2.proto import caffe2_pb2 as c2p2

from ModelHelpers import (
	TranslateSqueezenetModel,
	InitModel,
	RunModel
)
from Methods import PrintStatistics
from DatasetHelpers import LmdbDatasetWrapper# DatasetOnTheFly
from Constants import (
	labelsPath
)

lmdbPath = expanduser('~/workbench/tree-images/workspace/lmdb/train-augmented-dataset-lmdb-227')
imageMapPath = expanduser('~/workbench/tree-images/feature_labels_train.json')
squeezenetPath = expanduser('~/workbench/caffe2-models/squeezenet')
with open(labelsPath, 'r') as f:
	labels = json.load(f)

# devOps = core.DeviceOption(c2p2.PROTO_CUDA, 0)
devOps = c2p2.DeviceOption()
devOps.device_type = c2p2.PROTO_CUDA
devOps.device_id = 0
argScope = {
	'order': 'NCHW',
	'use_cudnn': True
}
model, deployNet = TranslateSqueezenetModel(
	'squeezenet',
	len(labels),
	join(squeezenetPath, 'init_net.pb'),
	join(squeezenetPath, 'predict_net.pb'),
	devOps,
	argScope
)

# print model.net.Proto()
print 'squeezenet model loaded'

datasetWrapper = LmdbDatasetWrapper(lmdbPath, 128, 227)# DatasetOnTheFly(imageMapPath, 128, 227)
datasetWrapper.Open()

# initialize data blobs
data, label = datasetWrapper[0]# .GetFirst()
workspace.FeedBlob('data', data)
workspace.FeedBlob('label', np.stack([label]).astype(np.int32))

def FeedData(batchIndex):
	datas, labels = datasetWrapper.GetBatch(batchIndex)
	workspace.FeedBlob('data', datas)
	workspace.FeedBlob('label', labels)

InitModel(model)

RunModel(
	model,
	1000,
	10,
	lambda i: FeedData(i),
	PrintStatistics
)


