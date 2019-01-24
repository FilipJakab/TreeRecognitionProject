

def Confirm(message):
	return raw_input(message + ' [[y]/n] ') in ['y', 'Y', 'yes', '']

def RunValidation(workspace, model, i):
	workspace.RunNet(model.net)
	PrintStatistics(workspace, i)

def PrintStatistics(workspace, i):
	acc = workspace.FetchBlob('accuracy')
	loss = workspace.FetchBlob('loss')

	print '%02d: acc: %.4f; loss: %.4f;' % (i, acc, loss)
