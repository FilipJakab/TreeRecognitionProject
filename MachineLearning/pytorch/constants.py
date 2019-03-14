from os.path import expanduser

import torchvision.transforms as transforms

modelTrainParamsPath = expanduser(
	'~/workbench/git/TreeRecognitionProject/MachineLearning/pytorch/deploy/train_params.pt'
)
modelDeployParamsPath = expanduser(
	'~/workbench/git/TreeRecognitionProject/MachineLearning/pytorch/deploy/deploy_params.onnx'
)
# production paths
# modelTrainParamsPath = expanduser(
# 	'~/workbench/dmp/MachineLearning/pytorch/deploy/train_params.pt'
# )
# modelDeployParamsPath = expanduser(
# 	'~/workbench/dmp/MachineLearning/pytorch/deploy/deploy_params.onnx'
# )

datasetLabelsPath = expanduser(
	'~/workbench/git/TreeRecognitionProject/MachineLearning/pytorch/deploy/labels.json'
)
# production path
# datasetLabelsPath = expanduser(
# 	'~/workbench/dmp/MachineLearning/pytorch/deploy/labels.json'
#)

dataDir = expanduser('~/workbench/tree-images/data/images')
batchSize = 64
learningRate = 1e-3
epochs = 3

trainTransformationFlow = transforms.Compose([
	transforms.RandomResizedCrop(224),
	transforms.RandomHorizontalFlip(),
	transforms.RandomVerticalFlip(),
	transforms.ToTensor(),
	transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

productionTransformationFlow = transforms.Compose([
	transforms.Resize(224),
	transforms.CenterCrop(224),
	transforms.ToTensor(),
	transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
