import skimage
import numpy as np
import cv2

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

def ChangeBrightness(img, value):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)

	limit = 255 - value
	v[v > limit] = 255
	v[v <= limit] += np.uint8(value)

	return cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)


AUGMENT_AMPLIFIER = 12
def AugmentImage(img, brightnessIndex=64, maxDeviation=32, deviationStep=8):

	deviatedImage = np.zeros((img.shape[0] + maxDeviation, img.shape[1] + maxDeviation, img.shape[2]), dtype=np.uint8)
	startX = (deviatedImage.shape[0]-img.shape[0])/2
	startY = (deviatedImage.shape[1]-img.shape[1])/2
	deviatedImage[startX:startX+img.shape[0], startY:startY+img.shape[1]] = img
	for y in range((maxDeviation / deviationStep) + 1):
		for x in range((maxDeviation / deviationStep) + 1):
			yDevStep = y*deviationStep # deviation in row
			xDevStep = x*deviationStep # deviation in col
			currentDeviatedImage = deviatedImage[yDevStep:(yDevStep)+img.shape[0], xDevStep:(xDevStep)+img.shape[1]]

			# flips - horizontal, vertical, and combined
			vFlipped = np.fliplr(currentDeviatedImage)
			hFlipped = np.flipud(currentDeviatedImage)
			hvFlipped = np.fliplr(hFlipped)

			# when this is changed AUGMENT_AMPLIFIER needs to be changed too
			# Its value is amount of yielded items
			yield currentDeviatedImage
			yield vFlipped
			yield hFlipped
			yield hvFlipped
			yield np.array(ChangeBrightness(currentDeviatedImage, brightnessIndex))
			yield np.array(ChangeBrightness(currentDeviatedImage, -brightnessIndex))
			yield np.array(ChangeBrightness(vFlipped, brightnessIndex))
			yield np.array(ChangeBrightness(vFlipped, -brightnessIndex))
			yield np.array(ChangeBrightness(hFlipped, brightnessIndex))
			yield np.array(ChangeBrightness(hFlipped, -brightnessIndex))
			yield np.array(ChangeBrightness(hvFlipped, brightnessIndex))
			yield np.array(ChangeBrightness(hvFlipped, -brightnessIndex))

def CalculateAugmentRatio(maxDeviation=32, deviationStep=8):
	return AUGMENT_AMPLIFIER * (((maxDeviation / deviationStep) + 1) ** 2)
