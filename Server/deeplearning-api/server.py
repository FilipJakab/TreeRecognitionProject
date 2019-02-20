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

def InsertLabels(imagesPredictions):
	with open(datasetLabelsPath, 'r') as f:
		labels = json.load(f)
	results = []
	for imagePrediction in imagesPredictions:
		prediction = {}
		print imagePrediction
		for label in labels.keys():
			prediction[label] = imagePrediction[labels[label]]
		results.append(prediction)
	return results

class RootController(Resource):
	def get(self):
		responseObj = {
			'data': '',
			'isOk': False,
			'taken': -1
		}

		
		if 'image' not in request.args.keys():
			responseObj['data'] = 'image was not provided'
			return responseObj

		images = request.args['image'].split(',')
		print 'images', images

		for image in images:
			if not os.path.isfile(image):
				print 'file at "%s" was not found..' % image
				responseObj['data'] = 'Specified file path "%s" was not found' % image
				return responseObj

		since = time.time()
		results = Run(images)
		softmaxedResults = SoftmaxFn(results)
		print 'softmaxedResults: ', softmaxedResults
		responseObj['data'] = InsertLabels(softmaxedResults)
		print 'data: ', responseObj['data']
		responseObj['taken'] = (time.time() - since)

		responseObj['isOk'] = True

		self.StringifyNumbers(responseObj)
		return responseObj

	def StringifyNumbers(self, obj):
		if type(obj) is list: 
			for i, item in enumerate(obj):
				obj[i] = str(item)
			return
		for key in obj.keys():
			if type(obj[key]) in [int, float]:
				obj[key] = str(obj[key])
			elif type(obj[key]) in [dict, list]:
				self.StringifyNumbers(obj[key])

	def check_file_extension(self, filename):
		return filename.split('.')[-1] in app.config['ALLOWED_IMAGE_EXETENSION']

class DemoController(Resource):
	"""docstring for DemoController"""
	def get(self):
		print request.args['image']
		

# example of method return
# return { 'message': '200 OK' }, 200, { 'custom-header': time.gmtime() }

api.add_resource(RootController, '/')
api.add_resource(DemoController, '/demo')

app.run(debug=True, host='0.0.0.0', port=3333)

