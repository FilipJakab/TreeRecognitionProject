imageSquaredDimension = 96
batchSize = 48
learningRate = 0.001
baseFolder = '/home/filip/workbench/tree-images'
trainLmdbPath = baseFolder + '/workspace/lmdb/train-ex-augmented-dataset-lmdb-{}'.format(imageSquaredDimension)
testLmdbPath = baseFolder + '/workspace/lmdb/test-ex-augmented-dataset-lmdb-{}'.format(imageSquaredDimension)
valLmdbPath = baseFolder + '/workspace/lmdb/val-ex-augmented-dataset-lmdb-{}'.format(imageSquaredDimension)
checkpointPath = baseFolder + '/checkpoints'
labelsPath = baseFolder + '/labels.json'
imageLabelMapPath = baseFolder + '/feature_labels.json'
trainImageLabelMapPath = baseFolder + '/feature_labels_train.json'
testImageLabelMapPath = baseFolder + '/feature_labels_test.json'
valImageLabelMapPath = baseFolder + '/feature_labels_val.json'
trainIters = 2000
statisticsEvery = 10
workspaceRootFolder = baseFolder + '/workspace'
initNetPath = baseFolder + '/workspace/saves/init_net_{}.pb'.format(imageSquaredDimension)
predictNetPath = baseFolder + '/workspace/saves/predict_net_{}.pb'.format(imageSquaredDimension)

squeezenetFolder = '/home/filip/workbench/caffe2-models/squeezenet'
