# from __future__ import print_function
import os, sys, time, json

import numpy as np
import io, skimage.io as io

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

# append my scripts to path if they are not already there
myPtorchScriptsPath = os.path.expanduser('../../MachineLearning/pytorch')
if myPtorchScriptsPath not in sys.path:
	sys.path.append(myPtorchScriptsPath)

# custom
from runtimePredictCaffe2 import Run
from functionImplementations import SoftmaxFn
from constants import datasetLabelsPath

app = Flask(__name__)
# set folder for uploading images
# app.config['UPLOAD_FOLDER'] = './upload_dir'
# app.config['ALLOWED_IMAGE_EXETENSION'] = set(['png', 'jpg', 'jpeg'])

api = Api(app)

def InsertLabels(singleImagePredictions):
	with open(datasetLabelsPath, 'r') as f:
		labels = json.load(f)
	result = {}
	for label in labels.keys():
		result[label] = singleImagePredictions[labels[label]]

	return result

class RootController(Resource):
	def get(self):
		responseObj = {
			'data': '',
			'isOk': False,
			'taken': -1
		}

		imagePath = request.args['image']

		if not os.path.isfile(imagePath):
			print 'file at "%s" was not found..' % imagePath
			responseObj['data'] = 'Specified file path "%s" was not found' % imagePath
			return responseObj

		since = time.time()
		responseObj['data'] = InsertLabels(SoftmaxFn(Run(imagePath)).tolist())
		responseObj['taken'] = (time.time() - since)

		print responseObj['data']

		responseObj['isOk'] = True
		return responseObj

	def check_file_extension(self, filename):
		return filename.split('.')[-1] in app.config['ALLOWED_IMAGE_EXETENSION']

# example of method return
# return { 'message': '200 OK' }, 200, { 'custom-header': time.gmtime() }

api.add_resource(RootController, '/')

app.run(debug=True, host='0.0.0.0', port=3333)

