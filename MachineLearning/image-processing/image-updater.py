'''
	Copies images from temp directory (path provided by arg)
	to the destination folder labeled by label provided by arg..
	each image gets new GUID and is registered to feature map json file
'''

from os.path import join, isfile, isdir, abspath, splitext
import json, sys
from shutil import move#, copyfile
from os import makedirs, listdir
import uuid

data_dir = sys.argv[1].rstrip('/')
label = sys.argv[2]

files = [join(data_dir, f) for f in listdir(data_dir) if isfile(join(data_dir, f))]

# dest_dir = abspath(dest_dir)

feature_label_path = 'data/feature_labels.json'
labels_path = 'data/labels.json'

features = []
if isfile(feature_label_path):
	with open(feature_label_path, 'r') as f:
		features = json.load(f)

labels = []
if isfile(labels_path):
	with open(labels_path, 'r') as f:
		labels = json.load(f)

if label not in labels:
	print 'label not created for these images'
	labels.append(label)
	makedirs(label)

for img in files:
	img_id = uuid.uuid4()
	new_filename = 'data/%s/%s%s' % (label, img_id, splitext(img)[1])
	print 'moving %s to %s' % (img, new_filename)
	move(img, new_filename)
	features.append([new_filename, labels.index(label)])

with open(labels_path, 'w') as f:
	json.dump(labels, f, indent=2)

with open(feature_label_path, 'w') as f:
	json.dump(features, f, indent=2)
