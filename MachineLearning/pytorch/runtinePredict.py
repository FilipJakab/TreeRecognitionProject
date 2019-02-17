'''
	runtime prediction script version with pytorch only..
'''

from os.path import expanduser

import torch
from torchvision import models

# configuration
from constants import (
	modelParamsPath
)

device = torch.device('cuda:0')

# init model
model = models.resnet18()

# load custom weights
model.load_state_dict(torch.load(modelParamsPath))

# load model to device
model = model.to(device)

# disable train-specific layers
model.train(False)
