import RPi.GPIO as IO
import time


IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(18, IO.IN)

while 1:
	print(IO.input(18))
	#time.sleep(0.5)
