import copy, torch
from os.path import isfile

from torch import nn
from torchvision import models

def InitModel_VGG(modelTrainParamsPath, classCount, device):
	trainParamsExists = isfile(modelTrainParamsPath)

	model = models.vgg13(pretrained=not trainParamsExists)
	if trainParamsExists:
		# reinit last FC layer to match dimensions from the saved state
		lastLayerInputSize = model.classifier[-1].in_features
		model.classifier[-1] = nn.Linear(lastLayerInputSize, classCount)

		model.load_state_dict(torch.load(modelTrainParamsPath))
		print 'model\'s weights were loaded from pytorch file: "%s"' % modelTrainParamsPath

		# freeze all layers
		for param in model.parameters():
			param.requires_grad = False

		# unfreeze last layer
		for param in model.classifier[-1].parameters():
			param.requires_grad = True
	else:
		# freeze all current layers
		for param in model.parameters():
			param.requires_grad = False

		# reinit last FC layer (new Modules have enabled grad by default...)
		lastLayerInputSize = model.classifier[-1].in_features
		model.classifier[-1] = nn.Linear(lastLayerInputSize, classCount)
	return model.to(device=device)

def InitModel_AlexNet(modelTrainParamsPath, classCount, device):
	trainParamsExists = isfile(modelTrainParamsPath)

	model = models.alexnet(pretrained=not trainParamsExists)
	if trainParamsExists:
		# reinit last FC layer to match dimensions from the saved state
		lastLayerInputSize = model.classifier[-1].in_features
		model.classifier[-1] = nn.Linear(lastLayerInputSize, classCount)

		model.load_state_dict(torch.load(modelTrainParamsPath))
		print 'model\'s weights were loaded from pytorch file: "%s"' % modelTrainParamsPath

		# freeze all layers
		for param in model.parameters():
			param.requires_grad = False

		# unfreeze last layer
		for param in model.classifier[-1].parameters():
			param.requires_grad = True
	else:
		# freeze all current layers
		for param in model.parameters():
			param.requires_grad = False

		# reinit last FC layer (new Modules have enabled grad by default...)
		lastLayerInputSize = model.classifier[-1].in_features
		model.classifier[-1] = nn.Linear(lastLayerInputSize, classCount)
	return model.to(device=device)

def InitModel(modelTrainParamsPath, classCount, device):
	trainParamsExists = isfile(modelTrainParamsPath)

	model = models.resnet34(pretrained=not trainParamsExists)
	if trainParamsExists:
		# reinit last FC layer to match dimensions from the saved state
		lastLayerInputSize = model.fc.in_features
		model.fc = nn.Linear(lastLayerInputSize, classCount)

		model.load_state_dict(torch.load(modelTrainParamsPath))
		print 'model\'s weights were loaded from pytorch file: "%s"' % modelTrainParamsPath

		# freeze all layers
		# for param in model.parameters():
		# 	param.requires_grad = False

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
	# zaloha vah modelu
	weightsCheckpoint = copy.deepcopy(model.state_dict())
	bestAcc = 0.

	# prepnuti modelu do trenovaciho modu
	# tj. mod pri kterem se aktualizuji vahy (v testovem, ci validacnim se optimizer nepouziva)
	model.train()
	# trenovani nekolikrat vsechny obrazky
	for epoch in range(epochs):
		scheduler.step()

		sumLoss, sumCorrcects = 0., 0

		# postupna iterace nad vesmi obrazky
		for data, label in loader:
			# preneseni batche z RAM do zarizeni (pravdepodobne pamet GPU)
			data = data.to(device=device)
			label = label.to(device=device)

			# clear gradients -> on each grad calculation -> grads are incremented
			# pro kazdy batch musi byt hodnoty gradientu vynulovany
			optimizer.zero_grad()
			# forward pass
			# batch je prohnan modelem
			pred = model(data)
			_, preds = torch.max(pred, 1)

			# ziska se chybovost
			loss = lossFn(pred, label)

			# backpropagace (zpetna aktualizace vah)
			loss.backward()
			optimizer.step()

			# ukladani mezidat
			sumLoss += loss.item() * data.size(0)
			sumCorrcects += torch.sum(preds == label.data)

		print '%d/%d' % (epoch + 1, epochs)
		
		epochLoss = sumLoss / datasetSize
		epochAcc = sumCorrcects.double() / datasetSize
		print 'loss: %0.4f \nacc: %0.4f' % (epochLoss, epochAcc)

		# pokud jsou vysledky prozatim nejlepsi,
		# zaloha vsech vah
		if epochAcc > bestAcc:
			bestAcc = epochAcc
			weightsCheckpoint = copy.deepcopy(model.state_dict())

		print '_' * 20

	model.load_state_dict(weightsCheckpoint)

	return model
