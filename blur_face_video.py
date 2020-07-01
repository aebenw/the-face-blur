from pyimagesearch.face_blurring import anonymize_face_pixelate
from pyimagesearch.face_blurring import anonymize_face_simple
import numpy as np
import cv2
import os


def blur_vid(file_name):
	prototxtPath = os.path.sep.join([os.getcwd(), "face_detector/deploy.prototxt"])
	weightsPath = os.path.sep.join([os.getcwd(), "face_detector/res10_300x300_ssd_iter_140000.caffemodel"])
	net = cv2.dnn.readNet(prototxtPath, weightsPath)

	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	cap = cv2.VideoCapture(file_name)
	# Hacky way of renaming file
	a = file_name.rsplit('/')
	b = a[-1].rsplit('.')
	b[0] = b[0] + '-output'
	c = '.'.join(b)
	a[-1] = c
	output_path = '/'.join(a)

	print(output_path)


	width = int(cap.get(3)) if cap.isOpened() else 640
	height = int(cap.get(4)) if cap.isOpened() else 360

	out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30.0, (width, height))

	# loop over the frames from the video stream
	while cap.isOpened():
		try:
			ret, frame = cap.read()
			if frame is not None:
				blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
					(104.0, 177.0, 123.0))

				# pass the blob through the network and obtain the face detections
				net.setInput(blob)
				detections = net.forward()

				# loop over the detections
				for i in range(0, detections.shape[2]):
					# extract the confidence (i.e., probability) associated with
					# the detection
					confidence = detections[0, 0, i, 2]

					# filter out weak detections by ensuring the confidence is
					# greater than the minimum confidence
					if confidence > .5:
						# compute the (x, y)-coordinates of the bounding box for
						# the object
						box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
						(startX, startY, endX, endY) = box.astype("int")

						# extract the face ROI
						face = frame[startY:endY, startX:endX]
						face = anonymize_face_simple(face, factor=3.0)
						frame[startY:endY, startX:endX] = face

				# Writing Frame to new file
				out.write(frame)
			else:
				break
		except Exception as e:
			print("Error occurred", e)
			break

	# do a bit of cleanup
	print("calling clean up functions")
	out.release()
	cv2.destroyAllWindows()
	cap.release()
	return file_name
