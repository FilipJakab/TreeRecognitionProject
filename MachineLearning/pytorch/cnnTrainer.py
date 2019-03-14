'''
	Implements simple round of CNN model learning process
	- init data loaders
	- load model and 'translate' it if necessary
	- run training for x epochs (x times amount of dataset)

	TODO:
	- Create custom dataset wrapper for LMDB dataset format
'''

import os, time, json
from os.path import expanduser, isfile

# Pytorch related
import torch
import torch.nn as nn
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms

# custom
import ModelHelpers as MH

# set path to model weights download folder
os.environ['TORCH_MODEL_ZOO'] = expanduser('~/workbench/temp/pytorch-home')

# config
from constants import (
	modelTrainParamsPath,
	modelDeployParamsPath,
	datasetLabelsPath,
	trainTransformationFlow,
	dataDir,
	batchSize,
	learningRate,
	epochs
)

# preparing device
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# device = torch.device('cpu')

dataset = datasets.ImageFolder(dataDir, trainTransformationFlow)
dataLoader = torch.utils.data.DataLoader(dataset, batch_size=batchSize, shuffle=True, num_workers=4)
dataClasses = len(dataset.classes)
datasetSize = len(dataset)
# save labels
with open(datasetLabelsPath, 'w') as f:
	json.dump(dataset.class_to_idx, f, indent=2)

print 'dataset loader created. \
total classes: %d, total dataset size: %d, epochs: %d' % (dataClasses, datasetSize, epochs)

print 'train params exists: ', isfile(modelTrainParamsPath)

model = MH.InitModel(modelTrainParamsPath, dataClasses, device)
print 'model loaded to device: %s' % (torch.cuda.get_device_name(device) if device.type != 'cpu' else 'cpu')

# prepare stuff for training
lossFn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learningRate, momentum=0.9)
lrScheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

print 'starting training'
since = time.time()
model = MH.RunTraining(
	model,
	lossFn,
	optimizer,
	lrScheduler,
	dataLoader,
	datasetSize,
	epochs,
	device
)

print 'training done\n (%d seconds taken)' % int(time.time() - since)

if raw_input('Do you want to save model to "%s"? ' % modelTrainParamsPath) in ['y', 'Y', '', 'yes']:
	print 'saving..'
	torch.save(model.state_dict(), modelTrainParamsPath)

if raw_input('Do you want to export model to "%s"? ' % modelDeployParamsPath) in ['y', 'Y', '', 'yes']:
	print 'saving..'
	dummyData = torch.randn(1, 3, 224, 224, device=device)
	model.train(False)
	torch.onnx._export(model, dummyData, modelDeployParamsPath, export_params=True)
