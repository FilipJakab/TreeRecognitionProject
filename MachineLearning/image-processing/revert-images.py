from os.path import join, isfile, isdir, abspath
import json, sys
from shutil import move#, copyfile
from os import makedirs, listdir
import uuid

data_dir = sys.argv[1].rstrip('/')

files = [join(data_dir, f) for f in listdir(data_dir) if isfile(join(data_dir, f))]

# dest_dir = abspath(dest_dir)

feature_label_path = "feature_labels.json"
labels_path = "labels.json"

if isfile(feature_label_path):
	with open(feature_label_path, 'r') as f:
		features = json.load(f)

if isfile(labels_path):
	with open(labels_path, 'r') as f:
		labels = json.load(f)

for feature in features:
	label = labels[feature[1]]
	if not isdir(label):
		makedirs(label)
	target = '%s/%s' % (label, feature[0].split('/')[1])
	print 'copying %s to %s' % (feature[0], target)

	move(feature[0], target)

