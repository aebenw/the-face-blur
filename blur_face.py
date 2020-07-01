from pyimagesearch.face_blurring import anonymize_face_pixelate
from pyimagesearch.face_blurring import anonymize_face_simple
import numpy as np
import cv2
import os


def blur_image(file_name):
	# TODO: Make filepaths consts
	prototxtPath = os.path.sep.join([os.getcwd(), "face_detector/deploy.prototxt"])
	weightsPath = os.path.sep.join([os.getcwd(), "face_detector/res10_300x300_ssd_iter_140000.caffemodel"])
	net = cv2.dnn.readNet(prototxtPath, weightsPath)

	# load the input image from disk, clone it, and grab the image spatial
	# dimensions
	image = cv2.imread(file_name)
	(h, w) = image.shape[:2]

	# construct a blob from the image
	blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	print("[INFO] computing face detections...")
	net.setInput(blob)
	detections = net.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability)
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is greater
		# than the minimum confidence
		if confidence > .5:
			# compute the (x, y)-coordinates of the bounding box for the
			# object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# extract the face ROI
			face = image[startY:endY, startX:endX]
			face = anonymize_face_simple(face, factor=3.0)
			image[startY:endY, startX:endX] = face

	# display the original image and the output image with the blurred
	# face(s) side by side
	cv2.imwrite(file_name, image)
	# TODO: Had a return to stop script from completing, not sure if its needed
	return file_name