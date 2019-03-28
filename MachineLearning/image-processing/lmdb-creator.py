from DataHelpers import CreateLmdb

from os.path import join, expanduser

workbench = expanduser('~/workbench')

CreateLmdb(
	join(workbench, 'tree-images/data/temp/lmdb-demo'),
	join(workbench, 'tree-images/data/feature_labels_val.json'),
	128,
	saveFile=True
)

print 'done'
