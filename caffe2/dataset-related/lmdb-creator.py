from DataHelpers import CreateLmdb

from os.path import join, expanduser

workbench = expanduser('~/workbench')

CreateLmdb(
	join(workbench, 'temp/lmdb-demo'),
	join(workbench, 'tree-images/feature_labels_val.json'),
	128,
	saveFile=True
)

print 'done'
