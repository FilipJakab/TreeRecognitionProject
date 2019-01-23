import skimage

def CropCenter(img, dimension_size):
	width, heigth = img.shape[1], img.shape[0]
	start_heigth = (heigth / 2) - dimension_size / 2
	start_width = (width / 2) - dimension_size / 2

	return img[start_heigth:start_heigth + dimension_size, start_width:start_width + dimension_size]

def ResizeImage(img, imageDimension):
	imageRatio = img.shape[0] / float(img.shape[1]) # height / width
	# portrait
	if imageRatio > 1:
		img = skimage.transform.resize(
			img,
			(int(imageDimension * imageRatio), imageDimension),
			mode='constant',
			cval=0.0,
			anti_aliasing=True
		)
	elif imageRatio < 1:
		img = skimage.transform.resize(img,
			(imageDimension, int(imageDimension / imageRatio)),
			mode='constant',
			cval=0.0,
			anti_aliasing=True
		)
	else:
		img = skimage.transform.resize(img, 
			(imageDimension, imageDimension),
			mode='constant',
			cval=0.0,
			anti_aliasing=True
		)
	
	return img
