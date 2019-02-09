from os.path import expanduser

import torchvision.transforms as transforms

modelTrainParamsPath = expanduser('~/workbench/temp/pytorch_home/__custom_weights/train_params.pt')
modelDeployParamsPath = expanduser('~/workbench/temp/pytorch_home/__custom_weights/deploy_params.pt')

trainTransformationFlow = transforms.Compose([
	transforms.RandomResizedCrop(224),
	transforms.RandomHorizontalFlip(),
	transforms.RandomVerticalFlip(),
	transforms.ToTensor(),
	transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

deployTransformationFlow = transforms.Compose([
	transforms.Resize(224),
	transforms.CenterCrop(224),
	transforms.ToTensor(),
	transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
