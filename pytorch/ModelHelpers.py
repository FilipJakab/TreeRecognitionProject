import copy, torch
from os.path import isfile

from torch import nn
from torchvision import models

def InitModel(modelTrainParamsPath, classCount, device):
	trainParamsExists = isfile(modelTrainParamsPath)

	model = models.resnet18(pretrained=not trainParamsExists)
	if trainParamsExists:
		# reinit last FC layer to match dimensions from the saved state
		lastLayerInputSize = model.fc.in_features
		model.fc = nn.Linear(lastLayerInputSize, classCount)

		model.load_state_dict(torch.load(modelTrainParamsPath))
		print 'model\'s weights were loaded from pytorch file: "%s"' % modelTrainParamsPath

		# freeze all layers
		for param in model.parameters():
			param.requires_grad = False

		# unfreeze last layer
		for param in model.fc.parameters():
			param.requires_grad = True
	else:
		# freeze all current layers
		for param in model.parameters():
			param.requires_grad = False

		# reinit last FC layer (new Modules have enabled grad by default...)
		lastLayerInputSize = model.fc.in_features
		model.fc = nn.Linear(lastLayerInputSize, classCount)
	return model.to(device=device)

def RunTraining(model, lossFn, optimizer, scheduler, loader, datasetSize, epochs, device):
	weightsCheckpoint = copy.deepcopy(model.state_dict())
	bestAcc = 0.

	model.train()
	for epoch in range(epochs):
		scheduler.step()

		sumLoss, sumCorrcects = 0., 0

		for data, label in loader:
			data = data.to(device=device)
			label = label.to(device=device)

			# clear gradients -> on each grad calculation -> grads are incremented
			optimizer.zero_grad()
			# forward pass
			pred = model(data)
			_, preds = torch.max(pred, 1)
			loss = lossFn(pred, label)
			loss.backward()
			optimizer.step()

			sumLoss += loss.item() * data.size(0)
			sumCorrcects += torch.sum(preds == label.data)

		print '%d/%d' % (epoch + 1, epochs)
		
		epochLoss = sumLoss / datasetSize
		epochAcc = sumCorrcects.double() / datasetSize
		print 'loss: %0.4f \nacc: %0.4f' % (epochLoss, epochAcc)

		if epochAcc > bestAcc:
			bestAcc = epochAcc
			weightsCheckpoint = copy.deepcopy(model.state_dict())

		print '_' * 20

	model.load_state_dict(weightsCheckpoint)

	return model
