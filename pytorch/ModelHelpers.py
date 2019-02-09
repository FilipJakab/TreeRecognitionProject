import copy, torch

def RunTraining(model, lossFn, optimizer, scheduler, loader, datasetSize, epochs, device):
	weightsCheckpoint = copy.deepcopy(model.state_dict())
	bestAcc = 0.

	model.train()
	for epoch in range(epochs):
		print '%d/%d' % (epoch, epochs - 1)

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

		epochLoss = sumLoss / datasetSize
		epochAcc = sumCorrcects.double() / datasetSize
		print 'loss: %0.4f \nacc: %0.4f' % (epochLoss, epochAcc)

		if epochAcc > bestAcc:
			bestAcc = epochAcc
			weightsCheckpoint = copy.deepcopy(model.state_dict())

		print '_' * 20

	model.load_state_dict(weightsCheckpoint)

	return model
