# USAGE
# python blur_face_video.py --face face_detector --method simple
# python blur_face_video.py --face face_detector --method pixelated

# import the necessary packages
from pyimagesearch.face_blurring import anonymize_face_pixelate
from pyimagesearch.face_blurring import anonymize_face_simple
import numpy as np
import argparse
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True,
	help="path to face detector model directory")
ap.add_argument("-m", "--method", type=str, default="simple",
	choices=["simple", "pixelated"],
	help="face blurring/anonymizing method")
ap.add_argument("-b", "--blocks", type=int, default=20,
	help="# of blocks for the pixelated blurring method")
ap.add_argument("-file", "--file", type=str,
	help="# filepath to mp4")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNet(prototxtPath, weightsPath)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
cap = cv2.VideoCapture(args["file"])

width = int(cap.get(3)) if cap.isOpened() else 640
height = int(cap.get(4)) if cap.isOpened() else 360

out = cv2.VideoWriter('./examples/output.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30.0, (width, height))

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
				if confidence > args["confidence"]:
					# compute the (x, y)-coordinates of the bounding box for
					# the object
					box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
					(startX, startY, endX, endY) = box.astype("int")

					# extract the face ROI
					face = frame[startY:endY, startX:endX]

					# check to see if we are applying the "simple" face
					# blurring method
					if args["method"] == "simple":
						face = anonymize_face_simple(face, factor=3.0)

					# otherwise, we must be applying the "pixelated" face
					# anonymization method
					else:
						face = anonymize_face_pixelate(face,
							blocks=args["blocks"])

					# store the blurred face in the output image
					frame[startY:endY, startX:endX] = face

			# show the output frame
			cv2.imshow("Frame", frame)
			out.write(frame)
			key = cv2.waitKey(1) & 0xFF
		else:
			break
	except Exception as e:
		print("Error occurred", e)
		break

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
print("calling clean up functions")
out.release()
cv2.destroyAllWindows()
cap.release()
