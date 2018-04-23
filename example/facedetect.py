import io
import picamera
import cv2
import numpy


a = 1
while a == 1:
#Create a memory stream so photos doesn't need to be saved in a file
	stream = io.BytesIO()

#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)


	with picamera.PiCamera() as camera:
    		camera.resolution = (320, 240)
    		camera.capture(stream, format='jpeg')

#Convert the picture into a numpy array
	buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#Now creates an OpenCV image
	image = cv2.imdecode(buff, 1)

#Load a cascade file for detecting faces
	face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_alt.xml')

#Convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Look for faces in the image using the loaded cascade file
	faces = face_cascade.detectMultiScale(gray, 1.5, 3)

	print "Found "+str(len(faces))+" face(s)"

	if len(faces) == 1:
		a = 2
		cv2.imwrite('detectedface.jpeg',image)
