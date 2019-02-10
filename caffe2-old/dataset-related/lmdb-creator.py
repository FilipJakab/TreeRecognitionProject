from DataHelpers import EnsureLmdb

from os.path import join, expanduser

workbench = expanduser('~/workbench')

EnsureLmdb(
	join(workbench, 'temp/lmdb-demo'),
	join(workbench, 'tree-images/feature_labels_val.json'),
	128
	# saveFile=True
)

print 'done'
