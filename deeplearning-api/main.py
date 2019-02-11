from __future__ import print_function
import time
import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

app = Flask(__name__)
# set folder for uploading images
app.config['UPLOAD_FOLDER'] = './upload_dir'
app.config['ALLOWED_IMAGE_EXETENSION'] = set(['png', 'jpg', 'jpeg'])

api = Api(app)

class RootController(Resource):
	def post(self):
		response_obj = { 'message': '', 'isOk': False }
		print('request.files: ', request.files)
		if not ('image' in request.files.keys()):
			print('request doesnt meet correct structure -> request doesnt contain image part')
			response_obj['message'] = 'request doesnt contain file part named "image"'
			return response_obj

		image = request.files['image']

		if image and image.filename == '':
			print('request format error -> image name is empty')
			response_obj['message'] = 'image filename is empty'
			return response_obj

		image_filename = secure_filename(image.filename)

		if not self.check_file_extension(image_filename):
			print('image doesnt contain valid file extension')
			response_obj['message'] = 'image doesnt contain valid file extension'
			return response_obj

		image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
		response_obj['message'] = 'Successful'
		response_obj['isOk'] = True

		return response_obj
	def check_file_extension(self, filename):
		return filename.split('.')[-1] in app.config['ALLOWED_IMAGE_EXETENSION']

# example of method return
# return { 'message': '200 OK' }, 200, { 'custom-header': time.gmtime() }

api.add_resource(RootController, '/')

app.run(debug=True, host='0.0.0.0', port=3333)

