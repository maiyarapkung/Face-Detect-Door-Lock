from termcolor import colored as color
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
import sys


print "Welcome to " + color("Face Recognition Door Lock System", "yellow")

print color("[Connection]", "magenta") + "Connecting to FTP Site. . . "
try:
	session = ftplib.FTP('waws-prod-dm1-039.ftp.azurewebsites.windows.net', 'doorlocksite\maiyarap', 'A292141361a')
	print color("[Connection]", "magenta") + color("Successfully ", "green")  + "to connect to ftp doorlock site"
except:
	print color("[Error]", "red") + " Can't contact ftp server to upload file, Try to restart the application to connect to ftp server"
	exit()
time.sleep(1)
print color("[Notification]", "cyan") + "Starting Sensor detecting Mode"

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(18, IO.IN)
passstatus = 23
lockstatus = 24
doorstatus = 1
IO.setup(passstatus, IO.OUT)
IO.setup(lockstatus, IO.OUT)
IO.output(passstatus, IO.LOW)
IO.output(lockstatus, IO.LOW)


IO.output(passstatus, IO.LOW)
IO.output(lockstatus, IO.HIGH)



time.sleep(3)
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")
print("     ")


def sensordetect():
	a = 1
	print color("[Notification]", "cyan") + "Watting for object to detected by Sensor"
	while a == 1:
 		if(IO.input(18) == True):
			print color("[DoorLock System]", "yellow") + "Some object detected in sensor, Starting face detect application"
			a = 2			
			facedetect()
		#if(IO.input(18) == False):

			#print("No object detected")


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
				print color("[DoorLock System]", "yellow") + "Face Detected, Ready to upload to server"
					
				now = datetime.datetime.now()				
				time = now.microsecond
				filename = "%s.jpg" % time
				cv2.imwrite("facedetect/%s" % filename, image)

				#FTP upload Zone
				print color("[DoorLock System]", "yellow") + "Starting to upload file to ftp site"
				file = open("facedetect/%s" % filename, 'rb')
				storfile = "STOR /site/wwwroot/doordata/facedetect/%s" % filename
                                try:
					 session.storbinary(storfile , file)
				except:
					print color("[Error]", "red") + "Fail to upload file to FTP Site, Start uploading again"
					try:
						session.storbinary(storfile , file)
					except:
						print color("[Error]", "red") + "Can't upload file to FTP site, Please check your connection and try again"
						sys.exit()
									


				print color("[DoorLock System]", "yellow") + "Successfully to tranfer file via ftp to doorlock site"
				print color("[DoorLock System]", "yellow") + "Start face detect api"
				
				
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
				try:
        				response = requests.post(face_detect_url, params=params, headers=headers, json={"url": image_URL})
        			except:
					print color("[Error]", "red") + "Can't connect to api services, Starting to connect again"			
					try:
						response = requests.post(face_detect_url, params=params, headers=headers, json={"url": image_URL})
					except:
						print color("[Error]", "red") + "Can't Connect to api services, Check your connection and start the application again"
				faces = response.json() 
				#print(faces)
				for face in faces:
					detectfaceid = face["faceId"]
				print color("[DoorLock System]", "yellow") + "Successfully get faceid, Start face similar and confidence services"
				face_similar = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/findsimilars"
				#print(detectfaceid)

				similarparams = {
				"faceId" : detectfaceid,
				"largeFaceListId" : "doorlargefaceid",
				"maxNumOfCandidatesReturned" : "1",
				"mode" : "matchPerson"
				}

				getconfi = requests.post(face_similar, headers=headers, json=similarparams)
				similarresponse = getconfi.json()
				#print(similarresponse)	
				aabc = str(similarresponse)
				if aabc == "[]" :
					print color("[Authroization Services]", "magenta") + "Face not matched, Not authroized. . ."
                                        print color("[DoorLock System]", "yellow") + "Return to sensor detecting mode. . ."
                                        sensordetect()

				else:
					for confi in similarresponse:					
						if "confidence" in confi:
							confidence = confi["confidence"]
							if confidence >= 0.7:
								doorunlock()				
							else:
								print color("[Authroization Services]", "magenta") + "Face not matched, Not authroized. . ."
								print color("[DoorLock System]", "yellow") + "Return to sensor detecting mode. . ."
								sensordetect()
						else:
							print color("[Authroization Services]", "magenta") + "Face not matched, Not authroized. . ."
                                                        print color("[DoorLock System]", "yellow") + "Return to sensor detecting mode. . ."
                                                        sensordetect()

					
						



			print color("[DoorLock System]", "yellow") + "No face detected %d/15" % c		

		else:


			b = 2
			print color("[DoorLock System]", "yellow") + "Returning to Sensor detecting mode . . ."
			sensordetect()



		c += 1

def doorunlock():
	IO.output(passstatus, IO.HIGH)
	IO.output(lockstatus, IO.LOW)
	print color("[Authroization Services]", "magenta") + "Your face has been verified, Door has been unlock"

	time.sleep(10)

	IO.output(passstatus, IO.LOW)
	IO.output(lockstatus, IO.HIGH)
	print color("[Authroization Services]", "magenta") + "Door has been locked, Starting sensormode"
	time.sleep(2)
	sensordetect()


sensordetect()


