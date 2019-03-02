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
from runtimePredictCaffe2 import Predictor
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
		for label in labels.keys():
			prediction[label] = imagePrediction[labels[label]]
		results.append(prediction)
	return results

predictor = Predictor()
class RootController(Resource):
	def post(self):
		responseObj = {
			'data': [],
			'isOk': False,
			'taken': -1
		}
		# validate input
		imagesJson = json.loads(request.data)
		if 'Images' not in imagesJson.keys():
			responseObj['data'] = 'images were not provided'
			return responseObj, 400
		images = imagesJson['Images']
		# print 'images', images
		for image in images:
			if not os.path.isfile(image):
				# print 'file at "%s" was not found..' % image
				responseObj['data'] = 'Specified file path "%s" was not found' % image
				return responseObj
		since = time.time()
		results = predictor.Run(images)
		softmaxedResults = SoftmaxFn(results)
		# print 'softmaxedResults: ', softmaxedResults
		responseObj['data'] = InsertLabels(softmaxedResults)
		# print 'data: ', responseObj['data']
		responseObj['taken'] = int((time.time() - since) * 1000)
		responseObj['isOk'] = True
		self.StringifyNumbers(responseObj)
		return responseObj
	def StringifyNumbers(self, obj):	
		if type(obj) is list: 
			for i in range(len(obj)):
				if type(obj[i]) in [int, float, np.float32]:
					obj[i] = str(obj[i])
				elif type(obj[i]) in [dict, list]:
					self.StringifyNumbers(obj[i])
			return
		for key in obj.keys():
			valType = type(obj[key])
			if valType in [int, float, np.float32]:
				obj[key] = str(obj[key])
			elif valType in [dict, list]:
				self.StringifyNumbers(obj[key])

# class DemoController(Resource):
# 	"""docstring for DemoController"""
# 	def get(self):
# 		print request.args['image']
		

# example of method return
# return { 'message': '200 OK' }, 200, { 'custom-header': time.gmtime() }

api.add_resource(RootController, '/')
# api.add_resource(DemoController, '/demo')

app.run(debug=True, host='0.0.0.0', port=3333)

