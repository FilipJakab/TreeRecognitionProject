import os
from os.path import expanduser, isfile

# Pytorch related
import torch
import torch.nn as nn
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms

# custom
import ModelHelpers as MH

# set path to model weights download folder
os.environ['TORCH_MODEL_ZOO'] = expanduser('~/workbench/temp/pytorch_home')

# config
from constants import (
	modelTrainParamsPath,
	modelDeployParamsPath,
	trainTransformationFlow
)

dataDir = expanduser('~/workbench/tree-images/data/')
batchSize = 128
learningRate = 1e-3
epochs = 15

# setting up device
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
torch.cuda.set_device(device) # default device

dataset = datasets.ImageFolder(dataDir, trainTransformationFlow)
dataLoader = torch.utils.data.DataLoader(dataset, batch_size=batchSize, shuffle=True, num_workers=4)
dataClasses = len(dataset.classes)
datasetSize = len(dataset)
print 'dataset loader created. \
total classes: %d, total dataset size: %d, epochs: %d' % (dataClasses, datasetSize, epochs)

print 'train params exists: ', isfile(modelTrainParamsPath)
trainParamsExists = isfile(modelTrainParamsPath)


if trainParamsExists:
	model = models.resnet18(pretrained=False)

	# reinit last FC layer to match dimensions from the saved state
	lastLayerInputSize = model.fc.in_features
	model.fc = nn.Linear(lastLayerInputSize, dataClasses)

	model.load_state_dict(torch.load(modelTrainParamsPath))
	print 'model\'s weights were loaded from pytorch file: "%s"' % modelTrainParamsPath

	# freeze all layers
	for param in model.parameters():
		param.requires_grad = False

	# unfreeze last layer
	for param in model.fc.parameters():
		param.requires_grad = True
else:
	model = models.resnet18(pretrained=True)

	# freeze all current layers
	for param in model.parameters():
		param.requires_grad = False

	# reinit last FC layer (new Modules have enabled grad by default...)
	lastLayerInputSize = model.fc.in_features
	model.fc = nn.Linear(lastLayerInputSize, dataClasses)

model = model.to(device=device)
print 'model loaded to device: %s' % torch.cuda.get_device_name(device)

# prepare stuff for training
lossFn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learningRate, momentum=0.9)
lrScheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

print 'starting training'
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

print 'training done'

if raw_input('Do y want to save model to "%s"? ' % modelTrainParamsPath) in ['y', 'Y', '', 'yes']:
	torch.save(model.state_dict(), modelTrainParamsPath)

if raw_input('Do y want to export model to "%s"? ' % modelDeployParamsPath) in ['y', 'Y', '', 'yes']:
	dummyData = torch.randn(2, 3, 224, 224, device=device)
	torch.onnx.export(model, dummyData, modelDeployParamsPath)