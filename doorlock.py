
import requests
import io
import picamera
import cv2
import numpy
import RPi.GPIO as IO
import time
import ftplib
import datetime
import json

print("Welcome to Face Recognition Door Lock Syste")

print("Connecting to ftp site. . .")
try:
	session = ftplib.FTP('waws-prod-dm1-039.ftp.azurewebsites.windows.net', 'doorlocksite\maiyarap', 'A292141361a')
	print("Successfully to connect to ftp doorlock site")
except:
	print("Can't contact ftp server to upload file, Try to restart the application to connect to ftp server")
	exit()
time.sleep(1)
print("Starting Sensor detecting Mode")
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(18, IO.IN)
passstatus = 23
lockstatus = 24
doorstatus = 1
IO.setup(passstatus, IO.OUT)
IO.setup(lockstatus, IO.OUT)

IO.output(passstatus, IO.LOW)
IO.output(lockstatus, IO.HIGH)



time.sleep(3)



def sensordetect():
	a = 1
	while a == 1:
 		if(IO.input(18) == True):
			print("Some object detected in sensor, Starting face detect application")
			a = 2			
			facedetect()
		if(IO.input(18) == False):

			print("No object detected")


def facedetect():
	b = 1
	c = 1
	while b == 1:
		if c <= 15:
			stream = io.BytesIO()
			with picamera.PiCamera() as camera:
				camera.resolution = (320, 240)
				camera.capture(stream, format="jpeg")
		
			buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
			image = cv2.imdecode(buff, 1)
			face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_alt.xml")
			gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, 1.5, 3)

			if len(faces) == 1:
				b = 2
				print("Face Detected, Ready to upload to server")
					
				now = datetime.datetime.now()				
				time = now.microsecond
				filename = "%s.jpg" % time
				cv2.imwrite("facedetect/%s" % filename, image)

				#FTP upload Zone
				print("Starting to upload file to ftp site")
				file = open("facedetect/%s" % filename, 'rb')
				storfile = "STOR /site/wwwroot/doordata/facedetect/%s" % filename
                                session.storbinary(storfile , file)
				print("Successfully to tranfer file via ftp to doorlock site")
				print("Start face detect api")
				
				
				subscription_key = "cf9603e7edc841688cf897bd5b38eec2"
			        assert subscription_key
			
        			face_detect_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
        			image_URL = "https://doorlocksite.azurewebsites.net/doordata/facedetect/%s" % filename
        			headers = {
        			"Ocp-Apim-Subscription-Key" : subscription_key
        			}

        			params = {
        			"returnFaceId" : "true",
        			"returnFaceLandmarks" : "false",
        			}

        			response = requests.post(face_detect_url, params=params, headers=headers, json={"url": image_URL})
        			faces = response.json()        			
				for face in faces:
					print(face["faceId"])
					





			print("No face detected %d/15" % c)		

		else:


			b = 2
			print("Returning to Sensor detecting mode . . .")
			time.sleep(3)

			

			sensordetect()



		c += 1


sensordetect()
